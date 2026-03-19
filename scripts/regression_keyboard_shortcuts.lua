-- Regression: inventory keyboard-only controls remain wired + documented
-- Run: lua scripts/regression_keyboard_shortcuts.lua

local function fail(msg)
    io.stderr:write("[FAIL] " .. msg .. "\n")
    os.exit(1)
end

local function expect(cond, msg)
    if not cond then
        fail(msg)
    end
end

local function readFile(path)
    local f = assert(io.open(path, "rb"))
    local data = f:read("*a")
    f:close()
    return data
end

local src = readFile("src/inventory_ui.lua")

local keyBranches = {
    "key == \"up\"",
    "key == \"down\"",
    "key == \"left\"",
    "key == \"right\"",
    "key == \"home\"",
    "key == \"end\"",
    "key == \"pageup\"",
    "key == \"pagedown\"",
    "key == \"return\"",
    "key == \"backspace\"",
    "key == \"escape\"",
    "key == \"f1\"",
    "key == \"f5\"",
    "key == \"f9\"",
    "key == \"u\" or key == \"e\" or key == \"d\" or key == \"s\" or key == \"x\"",
}

for _, token in ipairs(keyBranches) do
    expect(src:find(token, 1, true) ~= nil, "missing files-panel key branch: " .. token)
end

local helpStrings = {
    "Up/Dn:Nav Enter:ActionMenu Bksp:UpDir U/E/D/S/X:Quick F1:Help F5:Sort",
    "Up/Dn:Select Enter:Run U/E/D/S/X:Quick Gray=LOCKED (see inline reason) Esc:Back",
    "HELP / KEY BINDINGS",
    "Tab / I     Toggle inventory",
    "G           Pickup item on player tile",
}

for _, snippet in ipairs(helpStrings) do
    expect(src:find(snippet, 1, true) ~= nil, "missing keyboard help copy: " .. snippet)
end

print("[PASS] keyboard shortcut wiring/help regression validated")
