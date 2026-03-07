#!/usr/bin/env python3
"""
Retag item tiles using Gemini 3.1 Flash-Lite Preview (vision).
Processes tiled_id >= 769 in item_tile_data_new.json.
"""

import json
import base64
import os
import sys
import time
from collections import deque
import requests

DATA_FILE = "item_tile_data_new.json"
TILES_DIR = "kenny1bit/tiles"
RETAG_MIN_ID = 704
VERIFIED_MAX_ID = 771

from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GEMINI_MODEL = "gemini-3.1-flash-lite-preview"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

BASE_PROMPT = """This is a 16x16 pixel game item sprite from a fantasy RPG tileset.
Classify this item with a single-word category and a short (1-3 word) description.

Categories: helmet, boots, gloves, armor, jacket, robe, shield, weapon, tool,
key, gem, potion, ring, scroll, book, food, bomb, necklace, coin, wand, bow,
arrow, belt, bag, bottle, crown, skull, bone, misc

Respond in JSON only: {"category": "...", "description": "..."}"""


def build_prompt(item, recent_results):
    """Build prompt with few-shot examples and optional verified hint."""
    parts = [BASE_PROMPT]

    if recent_results:
        lines = ["", "Here are some recently classified items for reference:"]
        for r in recent_results:
            lines.append(f"- tid={r['tid']}: category={r['category']}, description={r['description']}")
        parts.append("\n".join(lines))

    if item["tiled_id"] <= VERIFIED_MAX_ID:
        parts.append(
            f"\nThis tile was previously classified as: "
            f"category={item['category']}, description={item['description']}\n"
            f"You may confirm or correct this classification."
        )

    return "\n".join(parts)


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_tile_image_b64(row, col):
    path = os.path.join(TILES_DIR, f"tile_{row}_{col}.png")
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def call_vision_api(b64_image, prompt):
    payload = {
        "contents": [
            {
                "parts": [
                    {"inline_data": {"mime_type": "image/png", "data": b64_image}},
                    {"text": prompt},
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 100,
            "responseMimeType": "application/json",
        },
    }

    for attempt in range(3):
        resp = requests.post(
            GEMINI_URL,
            params={"key": GEMINI_API_KEY},
            json=payload,
            timeout=60,
        )
        if resp.status_code == 429:
            wait = 60
            print(f"    Rate limited (429), waiting {wait}s (attempt {attempt + 1}/3)")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        content = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        return json.loads(content)

    raise RuntimeError("Rate limited after 3 retries")


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit", type=int, default=0, help="Max items to process (0=all)"
    )
    args = parser.parse_args()

    data = load_data()
    items = data["items"]

    # Filter items that need retagging
    to_retag = [i for i, item in enumerate(items) if item["tiled_id"] >= RETAG_MIN_ID]
    if args.limit > 0:
        to_retag = to_retag[: args.limit]
    total = len(to_retag)
    print(f"Processing {total} items (tiled_id >= {RETAG_MIN_ID})")

    success = 0
    failed = 0
    recent_results = deque(maxlen=8)

    for count, idx in enumerate(to_retag, 1):
        item = items[idx]
        tid = item["tiled_id"]
        row, col = item["row"], item["col"]

        b64 = get_tile_image_b64(row, col)
        if b64 is None:
            print(f"  [{count}/{total}] tile_{row}_{col}.png NOT FOUND, skipping")
            failed += 1
            continue

        prompt = build_prompt(item, list(recent_results))

        try:
            result = call_vision_api(b64, prompt)
            cat = result.get("category", "misc").lower().strip()
            desc = result.get("description", "unknown").strip()

            old_cat = item["category"]
            old_desc = item["description"]
            item["category"] = cat
            item["description"] = desc

            # Checkpoint: save after each item
            save_data(data)

            recent_results.append({"tid": tid, "category": cat, "description": desc})

            print(
                f"  [{count}/{total}] tid={tid} ({row},{col}): "
                f"{old_cat}/{old_desc} -> {cat}/{desc}"
            )
            success += 1

        except Exception as e:
            print(f"  [{count}/{total}] tid={tid} ({row},{col}): FAILED - {e}")
            failed += 1

        # Rate limit: wait between requests
        if count < total:
            time.sleep(4)

    print(f"\nDone! Success: {success}, Failed: {failed}, Total: {total}")


if __name__ == "__main__":
    main()
