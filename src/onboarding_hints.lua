local OnboardingHints = {}

local WINDOW_SECONDS = 5 * 60
local ROTATE_SECONDS = 12

local state = {
    elapsed = 0,
    active = true,
    events = {
        moved = false,
        searched = false,
        pickup = false,
        inventory = false,
        build = false,
    }
}

local loopTips = {
    "LOOP: Fight -> Loot -> Disasm/Build -> Power Up",
    "TIP: Check Action Menu lock reasons before spending SRL",
    "TIP: Build preview shows USED materials + SRL have/need",
}

function OnboardingHints.reset()
    state.elapsed = 0
    state.active = true
    for key, _ in pairs(state.events) do
        state.events[key] = false
    end
end

function OnboardingHints.update(dt)
    if not state.active then
        return
    end

    state.elapsed = state.elapsed + (dt or 0)
    if state.elapsed >= WINDOW_SECONDS then
        state.active = false
    end
end

function OnboardingHints.mark(eventName)
    if not eventName or state.events[eventName] == nil then
        return
    end
    state.events[eventName] = true
end

function OnboardingHints.isActive()
    return state.active
end

function OnboardingHints.getState()
    return {
        elapsed = state.elapsed,
        active = state.active,
        events = {
            moved = state.events.moved,
            searched = state.events.searched,
            pickup = state.events.pickup,
            inventory = state.events.inventory,
            build = state.events.build,
        }
    }
end

function OnboardingHints.getHint()
    if not state.active then
        return nil
    end

    if not state.events.moved then
        return "MOVE: WASD to scout rooms and avoid pressure."
    end
    if not state.events.searched then
        return "SEARCH: Hold E near a lootbox to open it."
    end
    if not state.events.pickup then
        return "PICKUP: Stand on dropped item and press G."
    end
    if not state.events.inventory then
        return "INVENTORY: Press TAB/I for Action Menu."
    end
    if not state.events.build then
        return "BUILD: Press F9 in inventory, preview, then confirm."
    end

    local idx = math.floor(state.elapsed / ROTATE_SECONDS) % #loopTips + 1
    return loopTips[idx]
end

return OnboardingHints
