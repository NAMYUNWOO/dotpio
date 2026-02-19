local Portal = {}
local cooldown = false

-- 맵 전환 콜백: onLoad(targetMap, targetPortal)
Portal.onLoad = nil

function Portal.check(playerX, playerY, Map)
    local p = Map.getPortalAt(playerX, playerY)
    if p and not cooldown then
        cooldown = true
        if Portal.onLoad then
            Portal.onLoad(p.targetMap, p.targetPortal)
        end
    elseif not p then
        cooldown = false
    end
end

function Portal.resetCooldown()
    cooldown = false
end

function Portal.setCooldown()
    cooldown = true
end

return Portal
