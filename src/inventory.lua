local Items = require("src.items")

local Inventory = {}
Inventory.capacity = 30

function Inventory.new()
    local root = {
        type = "dir",
        name = "BACKPACK",
        children = {},
        parent = nil,
    }
    -- Default folders
    local folders = {"POTIONS", "WEAPONS", "SCROLLS"}
    for _, name in ipairs(folders) do
        local dir = {type = "dir", name = name, children = {}, parent = root}
        root.children[#root.children + 1] = dir
    end
    return {root = root, currentDir = root}
end

function Inventory.getTotalSize(inv)
    local total = 0
    local function walk(dir)
        for _, child in ipairs(dir.children) do
            if child.type == "file" then
                local def = Items.get(child.itemId)
                total = total + (def and def.size or 1) * child.count
            elseif child.type == "dir" then
                walk(child)
            end
        end
    end
    walk(inv.root)
    return total
end

function Inventory.addItem(inv, itemId, count)
    count = count or 1
    local def = Items.get(itemId)
    if not def then return false end

    -- Check capacity
    local currentSize = Inventory.getTotalSize(inv)
    if currentSize + def.size * count > Inventory.capacity then
        return false, "Inventory full"
    end

    local targetDir = inv.currentDir

    -- If stackable, look for existing stack in current dir
    if def.stackable then
        for _, child in ipairs(targetDir.children) do
            if child.type == "file" and child.itemId == itemId then
                local space = def.maxStack - child.count
                if space >= count then
                    child.count = child.count + count
                    return true
                elseif space > 0 then
                    child.count = def.maxStack
                    count = count - space
                end
            end
        end
    end

    -- Create new file node(s)
    while count > 0 do
        local stackCount = count
        if def.stackable and def.maxStack then
            stackCount = math.min(count, def.maxStack)
        elseif not def.stackable then
            stackCount = 1
        end
        -- Count existing files with same itemId for unique naming
        local idx = 0
        for _, child in ipairs(targetDir.children) do
            if child.type == "file" and child.itemId == itemId then
                idx = idx + 1
            end
        end
        local node = {
            type = "file",
            name = Items.dosName(itemId, idx),
            itemId = itemId,
            count = stackCount,
            parent = targetDir,
        }
        targetDir.children[#targetDir.children + 1] = node
        count = count - stackCount
    end
    return true
end

function Inventory.removeItem(inv, node, count)
    if node.type ~= "file" then return false end
    count = count or 1
    node.count = node.count - count
    if node.count <= 0 then
        local parent = node.parent
        for i, child in ipairs(parent.children) do
            if child == node then
                table.remove(parent.children, i)
                break
            end
        end
    end
    return true
end

function Inventory.useItem(inv, node, player)
    if node.type ~= "file" then return false end
    local def = Items.get(node.itemId)
    if not def or not def.onUse then return false, "Cannot use this item" end
    local ok, msg = def.onUse(player)
    if ok then
        Inventory.removeItem(inv, node, 1)
    end
    return ok, msg
end

function Inventory.createFolder(inv, name)
    name = name:upper():sub(1, 8)
    if #name == 0 then return false, "Invalid name" end
    -- Check for duplicate
    for _, child in ipairs(inv.currentDir.children) do
        if child.type == "dir" and child.name == name then
            return false, "Folder exists"
        end
    end
    local dir = {type = "dir", name = name, children = {}, parent = inv.currentDir}
    inv.currentDir.children[#inv.currentDir.children + 1] = dir
    return true
end

function Inventory.deleteFolder(inv, node)
    if node.type ~= "dir" then return false, "Not a folder" end
    if #node.children > 0 then return false, "Folder not empty" end
    local parent = node.parent
    if not parent then return false, "Cannot delete root" end
    for i, child in ipairs(parent.children) do
        if child == node then
            table.remove(parent.children, i)
            return true
        end
    end
    return false
end

function Inventory.moveItem(inv, node, targetDir)
    if node.type == "dir" then return false, "Cannot move folders" end
    if targetDir.type ~= "dir" then return false, "Target is not a folder" end
    -- Remove from old parent
    local parent = node.parent
    for i, child in ipairs(parent.children) do
        if child == node then
            table.remove(parent.children, i)
            break
        end
    end
    node.parent = targetDir
    targetDir.children[#targetDir.children + 1] = node
    return true
end

function Inventory.getContents(dir)
    local dirs = {}
    local files = {}
    for _, child in ipairs(dir.children) do
        if child.type == "dir" then
            dirs[#dirs + 1] = child
        else
            files[#files + 1] = child
        end
    end
    table.sort(dirs, function(a, b) return a.name < b.name end)
    table.sort(files, function(a, b) return a.name < b.name end)
    local result = {}
    for _, d in ipairs(dirs) do result[#result + 1] = d end
    for _, f in ipairs(files) do result[#result + 1] = f end
    return result
end

function Inventory.sortContents(dir, mode)
    -- mode: "name", "type", "size"
    local dirs = {}
    local files = {}
    for _, child in ipairs(dir.children) do
        if child.type == "dir" then
            dirs[#dirs + 1] = child
        else
            files[#files + 1] = child
        end
    end
    table.sort(dirs, function(a, b) return a.name < b.name end)
    if mode == "name" then
        table.sort(files, function(a, b) return a.name < b.name end)
    elseif mode == "type" then
        table.sort(files, function(a, b)
            local da, db = Items.get(a.itemId), Items.get(b.itemId)
            local ea = da and da.ext or ""
            local eb = db and db.ext or ""
            if ea ~= eb then return ea < eb end
            return a.name < b.name
        end)
    elseif mode == "size" then
        table.sort(files, function(a, b)
            local da, db = Items.get(a.itemId), Items.get(b.itemId)
            local sa = (da and da.size or 1) * a.count
            local sb = (db and db.size or 1) * b.count
            if sa ~= sb then return sa > sb end
            return a.name < b.name
        end)
    end
    dir.children = {}
    for _, d in ipairs(dirs) do dir.children[#dir.children + 1] = d end
    for _, f in ipairs(files) do dir.children[#dir.children + 1] = f end
end

function Inventory.getPath(dir)
    local parts = {}
    local node = dir
    while node do
        table.insert(parts, 1, node.name)
        node = node.parent
    end
    return "C:\\" .. table.concat(parts, "\\")
end

function Inventory.getAllDirs(root, excludeDir)
    local result = {}
    local function walk(dir, depth)
        if dir ~= excludeDir then
            result[#result + 1] = {dir = dir, depth = depth}
            for _, child in ipairs(dir.children) do
                if child.type == "dir" then
                    walk(child, depth + 1)
                end
            end
        end
    end
    walk(root, 0)
    return result
end

return Inventory
