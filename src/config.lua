local Config = {
    TILE     = 16,
    SCALE    = 3,
    TS_COLS  = 32,
    TS_SIZE  = 543,
    FOV_HALF = math.pi / 4,
    FOV_RANGE = 10,
    MOVE_CD  = 0.12,
    MAGIC_COST   = 2,
    MAGIC_DMG    = 2,
    MAGIC_FLY    = 0.15,
    ENEMY_COUNT  = 8,
    ITEM_COUNT   = 6,
    MP_ITEM_GID  = 817,

    -- Enemy AI
    ENEMY_MOVE_CD  = 0.35,
    ENEMY_ATK_CD   = 0.8,
    ENEMY_ATK_DMG  = 1,
    ENEMY_DETECT   = 7,
    ENEMY_CHASE    = 12,
    ENEMY_FLEE_HP  = 1,

    DIR8 = {
        {1,0},{1,1},{0,1},{-1,1},{-1,0},{-1,-1},{0,-1},{1,-1},
    },

    FLIP_H = 0x80000000,
    FLIP_V = 0x40000000,
    FLIP_D = 0x20000000,
}

function Config.stripFlipBits(raw)
    if raw == 0 then return 0 end
    if raw >= 0x80000000 then raw = raw - 0x80000000 end
    if raw >= 0x40000000 then raw = raw - 0x40000000 end
    if raw >= 0x20000000 then raw = raw - 0x20000000 end
    return raw
end

function Config.angleTo8Dir(angle)
    return Config.DIR8[math.floor((angle + math.pi/8) / (math.pi/4)) % 8 + 1]
end

return Config
