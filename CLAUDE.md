# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Love2D 기반 탑다운 로그라이크 게임. 부채꼴 FOV, A* 적 AI, 포탈 멀티맵 시스템, 12스탯 장비 시스템을 갖춘 타일 기반 던전 크롤러.

## Commands

```bash
# 맵 데이터 빌드 (tsx 타일 속성 변경 후 반드시 실행)
python3 gen_game_data.py

# 게임 실행
love .

# 자동 스크린샷 생성 (map04 / DOS inventory)
./scripts/capture_screenshots.sh

# 포탈 연결 검증 (targetMap/targetPortal 무결성)
python3 scripts/validate_portals.py

# AI 서버 실행 (아이템 AI 설명 생성용, 포트 8001)
# 게임 내 AiDescribe.init()에서 자동 시작됨 — 수동 실행 불필요
./bin/llama-server \
  -m models/Qwen3-4B-UD-Q4_K_XL.gguf \
  --alias "qwen3-4b" --ctx-size 4096 --port 8001 -ngl 99
```

테스트/린팅 미설정.

## Architecture

**모듈 구조 (`src/`):**

| 모듈 | 역할 |
|------|------|
| `config.lua` | 상수 (TILE=16, SCALE=3, FOV, 전투, AI 등) + 유틸 함수 |
| `map.lua` | 맵 데이터 로드/쿼리 (walkable, opaque, portals) |
| `tileset.lua` | 타일셋 이미지 로드, 쿼드 생성, FOV 디밍 렌더링 |
| `fov.lua` | 부채꼴 FOV 레이캐스트 (90도, 범위 10타일) |
| `player.lua` | 플레이어 상태/WASD 이동/마우스 에임/렌더, recalcStats() 장비 스탯 합산 |
| `entities.lua` | 적(8)/아이템(6) 스폰/렌더, EnemyAI 통합 |
| `enemy_ai.lua` | 적 AI — Jumper A* 경로탐색, 5상태 FSM (idle/patrol/chase/attack/flee), Stats 연동 |
| `combat.lua` | 근접(Space)/마법(좌클릭)/투사체/데미지플래시, ATK/INT/DEF 스탯 기반 데미지 |
| `stats.lua` | 스탯 시스템 코어 — 4물리(ATK/DEF/AGI/INT) + 8속성, 데미지/방어/이속 공식 |
| `stat_chart.lua` | 레이더 차트 시각화 — Catmull-Rom 스플라인, 4점(물리)/8점(속성) 차트 |
| `camera.lua` | 카메라 팔로우 (맵 경계 클램프) |
| `portal.lua` | 포탈 시스템 (쿨다운, onLoad 콜백으로 맵 전환) |
| `hud.lua` | HP/MP 바, 적 수, 컨트롤 안내 |
| `items.lua` | JSON 기반 180개 아이템 로드 (equip_slot, tileRow/tileCol), `item_tile_data.json` |
| `inventory.lua` | 인벤토리 데이터 (DOS 파일시스템 트리, 폴더/파일 CRUD) + 장비 슬롯 시스템 |
| `inventory_ui.lua` | DOS MDIR 스타일 인벤토리 UI + Hero 스탯 레이더 차트 + AI 아이템 Info 패널 |
| `dos_ui.lua` | DOS 텍스트모드 렌더러 (80x40 그리드, 16색 ANSI, 박스드로잉) |
| `ai_describe.lua` | AI 아이템 설명 매니저 (서버 자동 시작/종료, 캐시, 비동기 요청) |
| `ai_worker.lua` | love.thread 워커 — llama-server API 호출 + JSON 파싱 |

**AI 아이템 설명 시스템:**
- `ai_describe.lua` — llama-server 자동 시작/종료 + 비동기 AI 설명 요청 관리
- `ai_worker.lua` — love.thread 워커, curl로 llama-server `/v1/chat/completions` 호출
- `items.lua` — JSON 기반 180개 아이템 로드 (equip_slot, flat stats, tileRow/tileCol)
- `inventory_ui.lua` — Info 패널에서 AI 결과 (lore/traits/effect/rarity) 렌더링
- **흐름:** 인벤토리에서 아이템 선택 → `AiDescribe.request(itemId)` → 워커 스레드가 카테고리별 힌트 포함 프롬프트 생성 → llama-server 호출 → nested JSON 파싱 (brace depth counting) → flat stats 재조립 → 캐시 저장 → Info 패널에 표시
- **서버 관리:** `AiDescribe.init()`에서 health 체크 후 자동 시작, `love.quit()`에서 자동 종료 (게임이 시작한 경우만)
- **모델:** `models/Qwen3-4B-UD-Q4_K_XL.gguf` (4B 모델), 바이너리: `bin/llama-server`, 포트 8001
- **프롬프트:** `/no_think` 모드, 카테고리별 스탯 힌트, flat stats 구조
- **Fallback:** 서버 응답 실패 시 기본 설명 제공 (`fallback = true`)

**스탯 & 장비 시스템:**
- `stats.lua` — 12스탯: 4물리(ATK/DEF/AGI/INT) + 8속성(fire/ice/lightning/poison/holy/dark/arcane/physical)
- 공식: `damageAmount(atk, weapon_atk)`, `damageReduction(def)`, `moveSpeed(agi)`
- `stat_chart.lua` — 레이더 차트 (Catmull-Rom 스플라인), 4점(물리)/8점(속성) 모드
- `inventory.lua` — 장비 슬롯: weapon/armor/shield/helmet/boots/accessory
- `player.lua:recalcStats()` — 장착 장비의 flat stats 합산 → 전투/이동에 반영
- `item_tile_data.json` — 180개 아이템 데이터 (category, equip_slot, row/col, stats)

**외부 라이브러리:**
- `libs/jumper/` — A* 경로탐색 (enemy_ai.lua에서 사용)
- `libs/json.lua` — JSON 인코딩/디코딩 (AI 통신용)

**맵 데이터:**
- `maps/map_01.lua`, `map_02.lua`, `map_03.lua`, `map_04.lua` — `gen_game_data.py`가 TMX+TSX에서 자동 생성
- 4레이어: Ground, GroundDeco, Collision, Overlay
- 타일 속성: `dim=true` → dimTiles (FOV 차단), `occlude_ov=true` → occludeTiles (엔티티 반투명)

**드로우 순서:**
Ground → GroundDeco → Collision → Items → Enemies → DamageFlash → Player → Projectiles → Overlay → FOV호+크로스헤어 → HUD

## Key Data

- **에셋:** `Tilemap/tileset_legacy_transparent.png` (유일한 런타임 이미지)
- **빌드 소스:** `Tilemap/layerd_fantasy_*.tmx` + `Tilemap/tileset_colored.tsx`
- **`kenny1bit/`** 디렉토리는 별도 WFC 파이프라인 프로젝트 (런타임 미사용)
- **`tile_data.lua`** 존재하나 현재 게임에서 미사용

## Notes

- 한국어 프로젝트. 코드 주석/커밋은 한국어 또는 영어 혼용.
- `conf.lua`에서 창 크기 1280x720 설정.
- 맵 전환 시 적/아이템 재스폰, A* 그리드 재빌드됨.
