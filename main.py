import pygame
import sys
import json
import os
import math
import random

pygame.init()

SW, SH = 1280, 720
FPS = 60
SAVE_FILE = "save.json"

        
C_SKY        = (180, 220, 255)
C_GROUND     = (100, 160,  60)
C_DIRT       = ( 80, 120,  40)
C_WHITE      = (255, 255, 255)
C_BLACK      = (  0,   0,   0)
C_RED        = (220,  50,  50)
C_GREEN      = ( 50, 200,  80)
C_BLUE       = ( 60, 130, 230)
C_YELLOW     = (255, 210,  40)
C_ORANGE     = (240, 130,  30)
C_PURPLE     = (150,  60, 200)
C_GRAY       = (120, 120, 120)
C_DARK       = ( 30,  30,  40)
C_PANEL      = ( 20,  20,  30, 210)
C_HP_BG      = ( 60,  20,  20)
C_XP         = ( 80, 200, 240)

GROUND_Y = SH - 160

import os as _os
_bg_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "background.jpg")
BG_IMAGE = pygame.transform.scale(pygame.image.load(_bg_path), (SW, SH))

                                                             
CAT_SPRITES = {}
ENEMY_SPRITES = {}

def load_sprites():
    _dir = _os.path.dirname(_os.path.abspath(__file__))
    _basic_cat_path = _os.path.join(_dir, "basic cat.png")
    if _os.path.exists(_basic_cat_path):
        _img = pygame.image.load(_basic_cat_path).convert_alpha()
        CAT_SPRITES[0] = pygame.transform.scale(_img, (80, 80))
    _doge_path = _os.path.join(_dir, "doge.png")
    if _os.path.exists(_doge_path):
        _img = pygame.image.load(_doge_path).convert_alpha()
        ENEMY_SPRITES[0] = pygame.transform.scale(_img, (120, 120))
    _titan_cat_path = _os.path.join(_dir, "titan cat.png")
    if _os.path.exists(_titan_cat_path):
        _img = pygame.image.load(_titan_cat_path).convert_alpha()
        CAT_SPRITES[9] = pygame.transform.scale(_img, (130, 130))
    _tank_cat_path = _os.path.join(_dir, "tank cat.png")
    if _os.path.exists(_tank_cat_path):
        _img = pygame.image.load(_tank_cat_path).convert_alpha()
        CAT_SPRITES[1] = pygame.transform.scale(_img, (90, 90))
    _cow_cat_path = _os.path.join(_dir, "cow cat.png")
    if _os.path.exists(_cow_cat_path):
        _img = pygame.image.load(_cow_cat_path).convert_alpha()
        CAT_SPRITES[4] = pygame.transform.scale(_img, (80, 80))
    _gross_cat_path = _os.path.join(_dir, "gross cat.png")
    if _os.path.exists(_gross_cat_path):
        _img = pygame.image.load(_gross_cat_path).convert_alpha()
        CAT_SPRITES[3] = pygame.transform.scale(_img, (80, 80))
    _axe_cat_path = _os.path.join(_dir, "axe cat.png")
    if _os.path.exists(_axe_cat_path):
        _img = pygame.image.load(_axe_cat_path).convert_alpha()
        CAT_SPRITES[2] = pygame.transform.scale(_img, (80, 80))
    _snache_path = _os.path.join(_dir, "snache.png")
    if _os.path.exists(_snache_path):
        _img = pygame.image.load(_snache_path).convert_alpha()
        ENEMY_SPRITES[1] = pygame.transform.scale(_img, (80, 80))
    _those_guys_path = _os.path.join(_dir, "those guys.png")
    if _os.path.exists(_those_guys_path):
        _img = pygame.image.load(_those_guys_path).convert_alpha()
        ENEMY_SPRITES[2] = pygame.transform.scale(_img, (75, 75))
    _hippoe_path = _os.path.join(_dir, "hippoe.png")
    if _os.path.exists(_hippoe_path):
        _img = pygame.image.load(_hippoe_path).convert_alpha()
        ENEMY_SPRITES[3] = pygame.transform.scale(_img, (110, 110))
    _bun_bun_path = _os.path.join(_dir, "bun bun.png")
    if _os.path.exists(_bun_bun_path):
        _img = pygame.image.load(_bun_bun_path).convert_alpha()
        ENEMY_SPRITES[4] = pygame.transform.scale(_img, (130, 130))
    for _fname, _dict, _id, _sz in [
        ("Bird Nathan.png",   CAT_SPRITES,   5, 80),
        ("Fish Nathan.png",   CAT_SPRITES,   6, 80),
        ("Lizard Nathan.png", CAT_SPRITES,   7, 80),
        ("Dragon Nathan.png", CAT_SPRITES,   8, 100),
        ("Big Arun.png",      ENEMY_SPRITES, 3, 110),
        ("Angry Arun.png",    ENEMY_SPRITES, 5, 110),
        ("Hyper Arun.png",    ENEMY_SPRITES, 6, 100),
        ("Ninja Arun.png",    ENEMY_SPRITES, 7, 80),
    ]:
        _p = _os.path.join(_dir, _fname)
        if _os.path.exists(_p):
            _img = pygame.image.load(_p).convert_alpha()
            _dict[_id] = pygame.transform.scale(_img, (_sz, _sz))

CAT_DEFS = [
    {"id":0,  "name":"Nathan",        "cf_cost":0,   "hp":250,  "dmg":20,  "spd":2.0, "range":60,  "atk_cd":1.8, "color":(230,200,120), "shape":"round",  "size":28},
    {"id":1,  "name":"Tank Nathan",   "cf_cost":30,  "hp":800,  "dmg":12,  "spd":1.0, "range":55,  "atk_cd":2.2, "color":(140,180,230), "shape":"round",  "size":36},
    {"id":2,  "name":"Axe Nathan",    "cf_cost":20,  "hp":350,  "dmg":55,  "spd":2.2, "range":65,  "atk_cd":2.5, "color":(200, 80, 80), "shape":"square", "size":30},
    {"id":3,  "name":"Gross Nathan",  "cf_cost":25,  "hp":300,  "dmg":30,  "spd":1.5, "range":200, "atk_cd":2.0, "color":(180,230,120), "shape":"wide",   "size":32},
    {"id":4,  "name":"Cow Nathan",    "cf_cost":30,  "hp":400,  "dmg":40,  "spd":3.5, "range":70,  "atk_cd":1.5, "color":(240,240,200), "shape":"round",  "size":30},
    {"id":5,  "name":"Bird Nathan",   "cf_cost":35,  "hp":280,  "dmg":65,  "spd":2.8, "range":80,  "atk_cd":2.0, "color":(120,200,240), "shape":"tri",    "size":30},
    {"id":6,  "name":"Fish Nathan",   "cf_cost":40,  "hp":500,  "dmg":50,  "spd":2.0, "range":90,  "atk_cd":1.8, "color":( 80,160,200), "shape":"wide",   "size":34},
    {"id":7,  "name":"Lizard Nathan", "cf_cost":50,  "hp":600,  "dmg":80,  "spd":1.8, "range":300, "atk_cd":3.0, "color":( 80,200,120), "shape":"long",   "size":32},
    {"id":8,  "name":"Dragon Nathan", "cf_cost":60,  "hp":750,  "dmg":100, "spd":2.0, "range":250, "atk_cd":2.5, "color":(220, 80,200), "shape":"round",  "size":40},
    {"id":9,  "name":"Titan Nathan",  "cf_cost":80,  "hp":1500, "dmg":150, "spd":1.2, "range":75,  "atk_cd":3.5, "color":( 80, 80,180), "shape":"square", "size":50},
]

DEPLOY_ENERGY = [10, 15, 18, 14, 16, 20, 22, 25, 28, 35]

ENEMY_DEFS = [
    {"id":0, "name":"Arun",        "hp":120,  "dmg":8,   "spd":1.8, "range":55,  "atk_cd":1.5, "color":(220,170, 80), "size":26, "xp":5,  "shape":"round"},
    {"id":1, "name":"Speedy Arun", "hp":80,   "dmg":5,   "spd":3.0, "range":50,  "atk_cd":1.2, "color":(200,220,100), "size":22, "xp":3,  "shape":"tri"},
    {"id":2, "name":"Mini Arun",   "hp":60,   "dmg":3,   "spd":2.5, "range":45,  "atk_cd":1.0, "color":(180,200,140), "size":20, "xp":2,  "shape":"round"},
    {"id":3, "name":"Big Arun",    "hp":500,  "dmg":30,  "spd":1.2, "range":65,  "atk_cd":2.0, "color":(220,160,200), "size":40, "xp":20, "shape":"wide"},
    {"id":4, "name":"Huge Arun",   "hp":1200, "dmg":60,  "spd":0.8, "range":80,  "atk_cd":2.5, "color":(240,200,180), "size":50, "xp":40, "shape":"square"},
    {"id":5, "name":"Angry Arun",  "hp":800,  "dmg":45,  "spd":1.5, "range":70,  "atk_cd":2.0, "color":(180, 80, 80), "size":42, "xp":30, "shape":"round"},
    {"id":6, "name":"Hyper Arun",  "hp":600,  "dmg":35,  "spd":2.0, "range":60,  "atk_cd":1.8, "color":(230,150, 60), "size":38, "xp":25, "shape":"tri"},
    {"id":7, "name":"Ninja Arun",  "hp":300,  "dmg":20,  "spd":2.2, "range":55,  "atk_cd":1.5, "color":(160,200,240), "size":30, "xp":12, "shape":"round"},
]

STAGES = [
    {"name":"The First Clash",        "bg":(160,200,255), "enemy_base_hp":2000,  "waves":[(0,5,2.0,3.0),(2,8,1.5,15.0)]},
    {"name":"Arun Territory",         "bg":(150,190,250), "enemy_base_hp":3000,  "waves":[(0,6,1.8,2.0),(2,6,1.5,12.0),(1,3,2.5,20.0)]},
    {"name":"Battle on the Bridge",   "bg":(140,180,245), "enemy_base_hp":4000,  "waves":[(0,8,1.5,2.0),(7,4,2.0,10.0),(3,2,3.0,25.0)]},
    {"name":"Nathan's Revenge",       "bg":(130,160,200), "enemy_base_hp":5000,  "waves":[(1,6,2.0,2.0),(0,10,1.2,5.0),(3,3,3.0,20.0)]},
    {"name":"The Arun Invasion",      "bg":(120,150,195), "enemy_base_hp":6500,  "waves":[(1,8,1.8,2.0),(6,3,3.0,15.0),(3,4,2.5,25.0)]},
    {"name":"Chaos at the Crossroads","bg":(110,140,190), "enemy_base_hp":8000,  "waves":[(5,4,2.5,2.0),(3,5,2.0,10.0),(4,2,4.0,30.0)]},
    {"name":"No Man's Land",          "bg":(100,130,220), "enemy_base_hp":10000, "waves":[(6,4,2.5,2.0),(1,8,1.5,10.0),(4,3,3.5,25.0)]},
    {"name":"The Final Push",         "bg":( 90,120,215), "enemy_base_hp":13000, "waves":[(5,6,2.0,2.0),(6,4,2.5,12.0),(4,3,3.0,28.0)]},
    {"name":"Arun Stronghold",        "bg":( 80,110,210), "enemy_base_hp":16000, "waves":[(7,5,2.0,2.0),(5,6,1.8,10.0),(4,4,3.0,20.0)]},
    {"name":"The Last Stand",         "bg":( 60, 80,160), "enemy_base_hp":25000, "waves":[(4,2,5.0,3.0),(5,4,2.5,10.0),(6,4,2.5,20.0),(4,2,4.0,35.0)]},
]

DEFAULT_SAVE = {
    "cat_food": 20,
    "xp": 0,
    "unlocked_cats": [0],
    "cat_levels": {str(i): 1 for i in range(10)},
    "stages_cleared": [],
}

def load_save():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE) as f:
            data = json.load(f)
        for k, v in DEFAULT_SAVE.items():
            if k not in data:
                data[k] = v
        return data
    return dict(DEFAULT_SAVE)

def write_save(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

font_big   = pygame.font.SysFont("Chalkboard SE", 30, bold=True)
font_med   = pygame.font.SysFont("Chalkboard SE", 20)
font_small = pygame.font.SysFont("Chalkboard SE", 14)

def fit_font(text, max_width, start_size=14):
    """Return a font that fits text within max_width pixels."""
    size = start_size
    while size > 6:
        f = pygame.font.SysFont("Chalkboard SE", size)
        if f.size(text)[0] <= max_width:
            return f
        size -= 1
    return pygame.font.SysFont("Chalkboard SE", 6)

def draw_text(surf, text, x, y, font=None, color=C_WHITE, center=False, shadow=True):
    f = font or font_med
    if shadow:
        s = f.render(text, True, C_BLACK)
        surf.blit(s, (x+1, y+1) if not center else (x - s.get_width()//2+1, y+1))
    img = f.render(text, True, color)
    if center:
        surf.blit(img, (x - img.get_width()//2, y))
    else:
        surf.blit(img, (x, y))

def draw_bar(surf, x, y, w, h, val, mx, fg, bg=C_HP_BG, border=True):
    pygame.draw.rect(surf, bg, (x, y, w, h), border_radius=3)
    if mx > 0:
        fill = int(w * max(0, val) / mx)
        if fill > 0:
            pygame.draw.rect(surf, fg, (x, y, fill, h), border_radius=3)
    if border:
        pygame.draw.rect(surf, C_WHITE, (x, y, w, h), 1, border_radius=3)

def draw_unit_shape(surf, x, y, shape, size, color, facing=1):
    lighter = tuple(min(255, c+60) for c in color)
    darker  = tuple(max(0,   c-60) for c in color)
    if shape == "round":
        pygame.draw.circle(surf, color,   (x, y), size)
        pygame.draw.circle(surf, lighter, (x - size//4, y - size//4), size//3)
        pygame.draw.circle(surf, darker,  (x, y), size, 2)
        ex = x + facing * size//3
        pygame.draw.circle(surf, C_WHITE, (ex, y - size//5), size//5)
        pygame.draw.circle(surf, C_BLACK, (ex + facing*2, y - size//5), size//8)
    elif shape == "square":
        r = pygame.Rect(x - size, y - size, size*2, size*2)
        pygame.draw.rect(surf, color,   r, border_radius=6)
        pygame.draw.rect(surf, lighter, (r.x+4, r.y+4, r.w//2, r.h//3), border_radius=4)
        pygame.draw.rect(surf, darker,  r, 2, border_radius=6)
        ex = x + facing * size//2
        pygame.draw.circle(surf, C_WHITE, (ex, y - size//4), size//4)
        pygame.draw.circle(surf, C_BLACK, (ex + facing*2, y - size//4), size//6)
    elif shape == "tri":
        pts = [
            (x + facing*size, y),
            (x - facing*size//2, y - size),
            (x - facing*size//2, y + size),
        ]
        pygame.draw.polygon(surf, color, pts)
        pygame.draw.polygon(surf, darker, pts, 2)
    elif shape == "wide":
        r = pygame.Rect(x - size, y - size//2, size*2, size)
        pygame.draw.rect(surf, color,   r, border_radius=8)
        pygame.draw.rect(surf, lighter, (r.x+4, r.y+3, r.w//2, r.h//2), border_radius=4)
        pygame.draw.rect(surf, darker,  r, 2, border_radius=8)
        ex = x + facing * size * 2 // 3
        pygame.draw.circle(surf, C_WHITE, (ex, y - size//5), size//4)
        pygame.draw.circle(surf, C_BLACK, (ex + facing*2, y - size//5), size//6)
    elif shape == "long":
        r = pygame.Rect(x - size, y - size//3, int(size*2.5), size*2//3)
        pygame.draw.rect(surf, color,   r, border_radius=6)
        pygame.draw.rect(surf, darker,  r, 2, border_radius=6)
        ex = x + facing * size
        pygame.draw.circle(surf, C_WHITE, (ex, y - size//4), size//4)
        pygame.draw.circle(surf, C_BLACK, (ex + facing*2, y - size//4), size//6)

class Particle:
    def __init__(self, x, y, color, vx, vy, life, size=4):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.color = color
        self.life = self.max_life = life
        self.size = size

    def update(self, dt):
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.vy += 0.15 * dt * 60
        self.life -= dt
        return self.life > 0

    def draw(self, surf, cam_x):
        alpha = max(0, self.life / self.max_life)
        s = max(1, int(self.size * alpha))
        pygame.draw.circle(surf, self.color, (int(self.x - cam_x), int(self.y)), s)

particles = []

def emit(x, y, color, n=8):
    for _ in range(n):
        a = random.uniform(0, math.pi*2)
        spd = random.uniform(1.5, 4)
        particles.append(Particle(x, y, color,
                                   math.cos(a)*spd, math.sin(a)*spd - 1,
                                   random.uniform(0.4, 0.9),
                                   random.randint(3, 6)))

class Projectile:
    def __init__(self, x, y, target_x, speed, dmg, color, is_cannon=False):
        self.x, self.y = float(x), float(y)
        self.tx = target_x
        self.spd = speed
        self.dmg = dmg
        self.color = color
        self.is_cannon = is_cannon
        self.alive = True
        self.start_x = x
        self.dist = abs(target_x - x)
        self.traveled = 0.0

    def update(self, dt):
        step = self.spd * dt * 60
        dx = self.tx - self.x
        if abs(dx) < step + 2:
            self.x = self.tx
            self.alive = False
            return
        self.x += math.copysign(step, dx)
        self.traveled += step

    @property
    def arc_y(self):
        if self.dist == 0:
            return self.y
        t = self.traveled / max(self.dist, 1)
        arc = -math.sin(t * math.pi) * (50 if self.is_cannon else 20)
        return self.y + arc

    def draw(self, surf, cam_x):
        sx = int(self.x - cam_x)
        sy = int(self.arc_y)
        if self.is_cannon:
            pygame.draw.circle(surf, self.color, (sx, sy), 10)
            pygame.draw.circle(surf, C_WHITE,    (sx, sy), 10, 2)
        else:
            pygame.draw.circle(surf, self.color, (sx, sy), 5)

class Unit:
    def __init__(self, x, defn, level=1, is_enemy=False):
        self.x = float(x)
        self.defn = defn
        self.level = level
        self.is_enemy = is_enemy
        mult = 1 + 0.1 * (level - 1)
        self.max_hp  = int(defn["hp"]  * mult)
        self.hp      = self.max_hp
        self.dmg     = int(defn["dmg"] * mult)
        self.spd     = defn["spd"]
        self.range   = defn["range"]
        self.atk_cd  = defn["atk_cd"]
        self.atk_timer = 0.0
        self.alive   = True
        self.attacking = False
        self.hit_flash = 0.0
        self.y = GROUND_Y
        self.bob_t = random.uniform(0, math.pi*2)

    def update(self, dt, allies, enemies, projectiles, cam_x):
        self.atk_timer   = max(0, self.atk_timer - dt)
        self.hit_flash   = max(0, self.hit_flash - dt)
        self.bob_t += dt * 3
        targets = enemies
        nearest = None
        nearest_d = 9999
        for t in targets:
            if t.alive:
                d = abs(t.x - self.x)
                if d < nearest_d:
                    nearest_d = d
                    nearest = t
        if nearest and nearest_d <= self.range:
            self.attacking = True
            if self.atk_timer <= 0:
                self.atk_timer = self.atk_cd
                nearest.take_hit(self.dmg, projectiles, self.x)
        else:
            self.attacking = False
            dir = 1 if not self.is_enemy else -1
            self.x += dir * self.spd * dt * 60

    def take_hit(self, dmg, projectiles, src_x):
        self.hp -= dmg
        self.hit_flash = 0.12
        emit(self.x, self.y - self.defn["size"]//2, C_RED, 6)
        if self.hp <= 0:
            self.alive = False
            emit(self.x, self.y, self.defn["color"], 14)

    def draw(self, surf, cam_x):
        sx = int(self.x - cam_x)
        bob = math.sin(self.bob_t) * 2 if not self.attacking else 0
        sy = int(self.y - self.defn["size"] + bob)
        color = self.defn["color"]
        if self.hit_flash > 0:
            color = C_WHITE
        facing = 1 if not self.is_enemy else -1
        unit_id = self.defn.get("id")
        sprite_dict = ENEMY_SPRITES if self.is_enemy else CAT_SPRITES
        if unit_id in sprite_dict:
            sprite = sprite_dict[unit_id]
            if facing == 1:
                sprite = pygame.transform.flip(sprite, True, False)
            sw, sh = sprite.get_size()
                         
            shadow = pygame.Surface((sw, sh), pygame.SRCALPHA)
            shadow.fill((0, 0, 0, 0))
            for _dx, _dy in [(-2,2),(0,2),(2,2),(0,3)]:
                shadow.blit(sprite, (_dx, _dy))
            shadow.set_alpha(100)
            surf.blit(shadow, (sx - sw // 2, sy - sh // 2))
            surf.blit(sprite, (sx - sw // 2, sy - sh // 2))
        else:
            draw_unit_shape(surf, sx, sy, self.defn.get("shape","round"), self.defn["size"], color, facing)

class Base:
    def __init__(self, x, hp, color, is_enemy=False):
        self.x = float(x)
        self.hp = self.max_hp = hp
        self.color = color
        self.is_enemy = is_enemy
        self.alive = True
        self.hit_flash = 0.0

    def take_hit(self, dmg, projectiles=None, src_x=0):
        self.hp -= dmg
        self.hit_flash = 0.2
        emit(self.x, GROUND_Y - 40, C_RED, 12)
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            emit(self.x, GROUND_Y - 40, self.color, 20)

    def draw(self, surf, cam_x):
        sx = int(self.x - cam_x)
        color = C_WHITE if self.hit_flash > 0 else self.color
        self.hit_flash = max(0, self.hit_flash - 1/60)
        pygame.draw.rect(surf, color, (sx-30, GROUND_Y-120, 60, 120), border_radius=4)
        pygame.draw.rect(surf, tuple(max(0,c-40) for c in self.color),
                         (sx-30, GROUND_Y-120, 60, 120), 3, border_radius=4)
        for i in range(3):
            bx = sx - 22 + i*22
            pygame.draw.rect(surf, color, (bx, GROUND_Y-135, 14, 20), border_radius=2)
        pygame.draw.line(surf, (180,180,180), (sx, GROUND_Y-120), (sx, GROUND_Y-160), 2)
        fc = C_RED if self.is_enemy else C_BLUE
        pygame.draw.polygon(surf, fc, [(sx, GROUND_Y-160),(sx+20, GROUND_Y-150),(sx, GROUND_Y-140)])
        draw_bar(surf, sx-50, GROUND_Y-155, 100, 10, self.hp, self.max_hp,
                 C_GREEN if not self.is_enemy else C_RED)

class CatCannon:
    COOLDOWN = 20.0
    DAMAGE   = 500

    def __init__(self):
        self.timer = 0.0

    @property
    def ready(self):
        return self.timer <= 0

    def update(self, dt):
        self.timer = max(0, self.timer - dt)

    def fire(self, src_x, targets, projectiles):
        if not self.ready:
            return
        self.timer = self.COOLDOWN
        tx = None
        for t in targets:
            if t.alive:
                tx = t.x
                break
        if tx is None:
            return
        projectiles.append(Projectile(src_x, GROUND_Y - 80, tx,
                                       6, self.DAMAGE, C_YELLOW, is_cannon=True))

class WaveSpawner:
    def __init__(self, stage_def, spawn_x):
        self.spawn_x = spawn_x
        self.queue = []
        t = 0.0
        for wave in stage_def["waves"]:
            eid, count, interval, delay = wave
            wt = delay
            for i in range(count):
                self.queue.append((wt, eid))
                wt += interval
        self.queue.sort()
        self.elapsed = 0.0

    def update(self, dt, enemies):
        self.elapsed += dt
        while self.queue and self.queue[0][0] <= self.elapsed:
            _, eid = self.queue.pop(0)
            edef = ENEMY_DEFS[eid]
            enemies.append(Unit(self.spawn_x, edef, level=1, is_enemy=True))

shake_timer = 0.0
shake_mag   = 0.0

def trigger_shake(mag=6, dur=0.25):
    global shake_timer, shake_mag
    shake_timer = dur
    shake_mag   = mag

def get_shake():
    global shake_timer
    if shake_timer > 0:
        shake_timer -= 1/60
        return (random.randint(-int(shake_mag), int(shake_mag)),
                random.randint(-int(shake_mag), int(shake_mag)))
    return (0, 0)

class DeployBar:
    MAX_ENERGY = 100.0
    REGEN = 4.0

    def __init__(self, unlocked, cat_levels):
        self.energy = 0.0
        self.unlocked = unlocked
        self.cat_levels = cat_levels
        self.cooldowns = {i: 0.0 for i in range(10)}

    def update(self, dt):
        self.energy = min(self.MAX_ENERGY, self.energy + self.REGEN * dt)
        for k in self.cooldowns:
            self.cooldowns[k] = max(0.0, self.cooldowns[k] - dt)

    def can_deploy(self, cat_id):
        cost = DEPLOY_ENERGY[cat_id]
        return (cat_id in self.unlocked and
                self.energy >= cost and
                self.cooldowns[cat_id] <= 0)

    def deploy(self, cat_id, units, spawn_x, save):
        if not self.can_deploy(cat_id):
            return False
        cost = DEPLOY_ENERGY[cat_id]
        self.energy -= cost
        self.cooldowns[cat_id] = CAT_DEFS[cat_id]["atk_cd"] + 0.5
        lvl = self.cat_levels.get(str(cat_id), 1)
        units.append(Unit(spawn_x, CAT_DEFS[cat_id], level=lvl, is_enemy=False))
        return True

    def draw(self, surf, save):
        panel_h = 150
        panel_surf = pygame.Surface((SW, panel_h), pygame.SRCALPHA)
        panel_surf.fill((10, 10, 20, 200))
        surf.blit(panel_surf, (0, SH - panel_h))

        draw_text(surf, f"Energy: {int(self.energy)}/{int(self.MAX_ENERGY)}",
                  10, SH - panel_h + 8, font_small, C_XP)
        draw_bar(surf, 10, SH - panel_h + 26, 200, 12,
                 self.energy, self.MAX_ENERGY, C_XP, (30,30,60))

        visible = [i for i in range(10) if i in self.unlocked]
        for idx, cid in enumerate(visible[:8]):
            bx = 10 + idx * 100
            by = SH - panel_h + 50
            bw, bh = 90, 85

            cd = self.cooldowns[cid]
            can = self.can_deploy(cid)
            border_c = C_GREEN if can else C_GRAY
            bg_c = (30,50,30) if can else (30,30,30)

            pygame.draw.rect(surf, bg_c,    (bx, by, bw, bh), border_radius=6)
            pygame.draw.rect(surf, border_c,(bx, by, bw, bh), 2, border_radius=6)

            cdef = CAT_DEFS[cid]
            if cid in CAT_SPRITES:
                icon = pygame.transform.scale(CAT_SPRITES[cid], (44, 44))
                if not can:
                    dark = pygame.Surface((44, 44), pygame.SRCALPHA)
                    dark.fill((80, 80, 80, 160))
                    icon = icon.copy()
                    icon.blit(dark, (0, 0))
                surf.blit(icon, (bx + bw//2 - 22, by + 4))
            else:
                draw_unit_shape(surf, bx + bw//2, by + 28,
                                cdef.get("shape","round"), min(18, cdef["size"]//2),
                                cdef["color"] if can else C_GRAY, 1)

            name_font = fit_font(cdef["name"], bw - 6)
            draw_text(surf, cdef["name"], bx+4, by+50, name_font,
                      C_WHITE if can else C_GRAY, shadow=False)
            draw_text(surf, f"E:{DEPLOY_ENERGY[cid]}", bx+4, by+65, font_small,
                      C_YELLOW if can else C_GRAY, shadow=False)

            if cd > 0:
                ov = pygame.Surface((bw, bh), pygame.SRCALPHA)
                ov.fill((0,0,0,120))
                surf.blit(ov, (bx, by))
                draw_text(surf, f"{cd:.1f}s", bx + bw//2, by + bh//2 - 8,
                          font_small, C_WHITE, center=True, shadow=True)

            draw_text(surf, str(idx+1), bx+bw-14, by+3, font_small, (180,180,180), shadow=False)

        draw_text(surf, f"XP: {save['xp']}", SW-200, SH-panel_h+8, font_med, C_XP)
        draw_text(surf, f"Nathan Food: {save['cat_food']}", SW-200, SH-panel_h+34, font_med, C_YELLOW)

class BattleScene:
    WORLD_W = 1280
    CAT_SPAWN_X = 250

    def __init__(self, stage_idx, save, screen):
        self.stage_idx = stage_idx
        self.save = save
        self.screen = screen
        self.stage = STAGES[stage_idx]
        self.result = None

        self.cam_x = 0.0
        self.units = []
        self.projectiles = []
        self.particles_local = particles

        self.player_base = Base(150, 5000, C_BLUE, is_enemy=False)
        self.enemy_base  = Base(self.WORLD_W - 150, self.stage["enemy_base_hp"],
                                C_RED, is_enemy=True)

        self.spawner = WaveSpawner(self.stage, self.WORLD_W - 200)
        self.cannon  = CatCannon()
        self.deploy  = DeployBar(save["unlocked_cats"], save.get("cat_levels", {}))
        self.xp_gained = 0
        self.result_timer = 0.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            for i in range(8):
                if event.key == pygame.K_1 + i:
                    vis = [c for c in range(10) if c in self.save["unlocked_cats"]]
                    if i < len(vis):
                        self.deploy.deploy(vis[i], self.units, self.CAT_SPAWN_X, self.save)
            if event.key == pygame.K_SPACE:
                self.cannon.fire(self.player_base.x + 30,
                                 sorted([u for u in self.units if u.is_enemy and u.alive],
                                        key=lambda u: u.x),
                                 self.projectiles)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            vis = [c for c in range(10) if c in self.save["unlocked_cats"]]
            panel_h = 150
            for idx, cid in enumerate(vis[:8]):
                bx = 10 + idx * 100
                by = SH - panel_h + 50
                if bx <= mx <= bx+90 and by <= my <= by+85:
                    self.deploy.deploy(cid, self.units, self.CAT_SPAWN_X, self.save)
            if SW-120 <= mx <= SW-10 and 10 <= my <= 60:
                self.cannon.fire(self.player_base.x + 30,
                                 sorted([u for u in self.units if u.is_enemy and u.alive],
                                        key=lambda u: u.x),
                                 self.projectiles)

    def update(self, dt):
        if self.result:
            self.result_timer += dt
            return

        self.deploy.update(dt)
        self.cannon.update(dt)

        cats    = [u for u in self.units if not u.is_enemy and u.alive]
        enemies = [u for u in self.units if u.is_enemy     and u.alive]

        self.spawner.update(dt, self.units)

        for u in self.units:
            if u.alive:
                if not u.is_enemy:
                    u.update(dt, cats, enemies + [self.enemy_base], self.projectiles, self.cam_x)
                    if abs(u.x - self.enemy_base.x) <= u.range and self.enemy_base.alive:
                        if u.atk_timer <= 0:
                            u.atk_timer = u.atk_cd
                            self.enemy_base.take_hit(u.dmg)
                            if not self.enemy_base.alive:
                                trigger_shake(10, 0.5)
                else:
                    u.update(dt, enemies, cats + [self.player_base], self.projectiles, self.cam_x)
                    if abs(u.x - self.player_base.x) <= u.range and self.player_base.alive:
                        if u.atk_timer <= 0:
                            u.atk_timer = u.atk_cd
                            self.player_base.take_hit(u.dmg)
                            if not self.player_base.alive:
                                trigger_shake(10, 0.5)

        for p in self.projectiles:
            p.update(dt)
            if not p.alive:
                targets = ([u for u in self.units if u.is_enemy and u.alive]
                           + ([self.enemy_base] if self.enemy_base.alive else []))
                for t in targets:
                    if abs(t.x - p.tx) < 60:
                        t.take_hit(p.dmg, self.projectiles, p.start_x)
                        trigger_shake(4, 0.15)
                        break

        for u in self.units:
            if not u.alive and u.is_enemy and hasattr(u, '_xp_given') is False:
                u._xp_given = True
                self.xp_gained += u.defn.get("xp", 5)

        self.projectiles = [p for p in self.projectiles if p.alive]
        self.units = [u for u in self.units if u.alive or not hasattr(u, '_xp_given')]

        front_cats = [u.x for u in self.units if not u.is_enemy and u.alive]
        if front_cats:
            target_cam = max(front_cats) - SW * 0.4
        else:
            target_cam = 0
        self.cam_x += (target_cam - self.cam_x) * 0.05
        self.cam_x = max(0, min(self.WORLD_W - SW, self.cam_x))

        if not self.enemy_base.alive:
            self.result = "win"
            self.save["xp"] += self.xp_gained + 10
            self.save["cat_food"] += 20
            if self.stage_idx not in self.save["stages_cleared"]:
                self.save["stages_cleared"].append(self.stage_idx)
            write_save(self.save)
        elif not self.player_base.alive:
            self.result = "lose"

    def draw_background(self):
        self.screen.blit(BG_IMAGE, (0, 0))

    def draw(self):
        self.draw_background()

        sx, sy = get_shake()

        self.player_base.draw(self.screen, self.cam_x - sx)
        self.enemy_base.draw(self.screen, self.cam_x - sx)

        for u in sorted(self.units, key=lambda u: u.x):
            if u.alive:
                u.draw(self.screen, self.cam_x - sx)

        for p in self.projectiles:
            p.draw(self.screen, self.cam_x - sx)

        particles[:] = [p for p in particles if p.update(1/60)]
        for p in particles:
            p.draw(self.screen, self.cam_x - sx)

        self.deploy.draw(self.screen, self.save)

        ready = self.cannon.ready
        cc = C_YELLOW if ready else C_GRAY
        pygame.draw.rect(self.screen, (30,30,10) if ready else (20,20,20),
                         (SW-120, 10, 110, 50), border_radius=8)
        pygame.draw.rect(self.screen, cc, (SW-120, 10, 110, 50), 2, border_radius=8)
        draw_text(self.screen, "CANNON", SW-65, 18, font_med, cc, center=True)
        if not ready:
            draw_text(self.screen, f"{self.cannon.timer:.1f}s", SW-65, 38,
                      font_small, C_GRAY, center=True)
        else:
            draw_text(self.screen, "[SPACE]", SW-65, 38, font_small, C_YELLOW, center=True)

        if self.result:
            ov = pygame.Surface((SW, SH), pygame.SRCALPHA)
            ov.fill((0,0,0,160))
            self.screen.blit(ov, (0,0))
            if self.result == "win":
                draw_text(self.screen, "you won!", SW//2, SH//2 - 60,
                          font_big, C_YELLOW, center=True)
                draw_text(self.screen, f"+20 nathan food  +{self.xp_gained+10} xp",
                          SW//2, SH//2, font_med, C_XP, center=True)
            else:
                draw_text(self.screen, "you lost...", SW//2, SH//2 - 60,
                          font_big, C_RED, center=True)
            draw_text(self.screen, "press enter to go back",
                      SW//2, SH//2 + 50, font_med, C_WHITE, center=True)

class ShopScene:
    def __init__(self, save, screen):
        self.save = save
        self.screen = screen
        self.message = ""
        self.msg_timer = 0.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for idx, cdef in enumerate(CAT_DEFS):
                col = idx % 5
                row = idx // 5
                bx = 60 + col * 230
                by = 140 + row * 220
                if bx <= mx <= bx+200 and by <= my <= by+190:
                    self._buy(cdef["id"])

    def _buy(self, cid):
        cdef = CAT_DEFS[cid]
        if cid in self.save["unlocked_cats"]:
            self.message = f"{cdef['name']} already owned!"
            self.msg_timer = 2.0
            return
        if self.save["cat_food"] < cdef["cf_cost"]:
            self.message = f"Need {cdef['cf_cost']} Nathan Food!"
            self.msg_timer = 2.0
            return
        self.save["cat_food"] -= cdef["cf_cost"]
        self.save["unlocked_cats"].append(cid)
        write_save(self.save)
        self.message = f"Unlocked {cdef['name']}!"
        self.msg_timer = 2.0

    def update(self, dt):
        self.msg_timer = max(0, self.msg_timer - dt)

    def draw(self):
        self.screen.fill(C_DARK)
        draw_text(self.screen, "Nathan Shop", SW//2, 20, font_big, C_YELLOW, center=True)
        draw_text(self.screen, f"nathan food: {self.save['cat_food']}",
                  SW//2, 60, font_med, C_YELLOW, center=True)
        draw_text(self.screen, "click a Nathan to unlock it  —  basic Nathan is free",
                  SW//2, 90, font_small, C_GRAY, center=True)

        for idx, cdef in enumerate(CAT_DEFS):
            col = idx % 5
            row = idx // 5
            bx = 60 + col * 230
            by = 140 + row * 220
            owned = cdef["id"] in self.save["unlocked_cats"]
            can   = not owned and self.save["cat_food"] >= cdef["cf_cost"]

            bg    = (20,40,20) if owned else ((30,30,50) if can else (25,20,20))
            border= C_GREEN if owned else (C_BLUE if can else C_GRAY)
            pygame.draw.rect(self.screen, bg,     (bx, by, 200, 190), border_radius=10)
            pygame.draw.rect(self.screen, border, (bx, by, 200, 190), 2, border_radius=10)

            if cdef["id"] in CAT_SPRITES:
                icon = pygame.transform.scale(CAT_SPRITES[cdef["id"]], (70, 70))
                self.screen.blit(icon, (bx + 65, by + 20))
            else:
                draw_unit_shape(self.screen, bx+100, by+65, cdef.get("shape","round"),
                                cdef["size"]//2+8, cdef["color"], 1)

            draw_text(self.screen, cdef["name"],  bx+100, by+100, font_med, C_WHITE, center=True)
            draw_text(self.screen, f"HP:{cdef['hp']} DMG:{cdef['dmg']}", bx+100, by+125,
                      font_small, C_GRAY, center=True)
            draw_text(self.screen, f"SPD:{cdef['spd']} RNG:{cdef['range']}", bx+100, by+143,
                      font_small, C_GRAY, center=True)

            if owned:
                draw_text(self.screen, "OWNED", bx+100, by+163, font_med, C_GREEN, center=True)
            else:
                draw_text(self.screen, f"{cdef['cf_cost']} Nathan Food", bx+100, by+163,
                          font_med, C_YELLOW if can else C_GRAY, center=True)

        if self.msg_timer > 0:
            draw_text(self.screen, self.message, SW//2, SH-50, font_big, C_YELLOW, center=True)

class UpgradeScene:
    LEVEL_COST = [0, 30, 60, 100, 150, 210, 280, 360, 450, 550]
    MAX_LEVEL  = 10

    def __init__(self, save, screen):
        self.save = save
        self.screen = screen
        self.message = ""
        self.msg_timer = 0.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for idx in range(10):
                if idx not in self.save["unlocked_cats"]:
                    continue
                col = idx % 5
                row = idx // 5
                bx = 60 + col * 230
                by = 140 + row * 210
                ubx, uby = bx + 50, by + 150
                if ubx <= mx <= ubx+100 and uby <= my <= uby+30:
                    self._upgrade(idx)

    def _upgrade(self, cid):
        lvl = self.save["cat_levels"].get(str(cid), 1)
        if lvl >= self.MAX_LEVEL:
            self.message = "Already max level!"
            self.msg_timer = 2.0
            return
        cost = self.LEVEL_COST[lvl]
        if self.save["xp"] < cost:
            self.message = f"Need {cost} XP!"
            self.msg_timer = 2.0
            return
        self.save["xp"] -= cost
        self.save["cat_levels"][str(cid)] = lvl + 1
        write_save(self.save)
        cname = CAT_DEFS[cid]["name"]
        self.message = f"{cname} -> Lv {lvl+1}!"
        self.msg_timer = 2.0

    def update(self, dt):
        self.msg_timer = max(0, self.msg_timer - dt)

    def draw(self):
        self.screen.fill(C_DARK)
        draw_text(self.screen, "Upgrades", SW//2, 20, font_big, C_XP, center=True)
        draw_text(self.screen, f"xp: {self.save['xp']}",
                  SW//2, 60, font_med, C_XP, center=True)
        draw_text(self.screen, "unlock a Nathan first to upgrade it",
                  SW//2, 90, font_small, C_GRAY, center=True)

        for idx in range(10):
            col = idx % 5
            row = idx // 5
            bx = 60 + col * 230
            by = 140 + row * 210
            cdef = CAT_DEFS[idx]
            owned = idx in self.save["unlocked_cats"]
            lvl   = self.save["cat_levels"].get(str(idx), 1)
            cost  = self.LEVEL_COST[lvl] if lvl < self.MAX_LEVEL else None

            bg = (20,20,40) if owned else (15,15,20)
            pygame.draw.rect(self.screen, bg,     (bx, by, 200, 190), border_radius=10)
            pygame.draw.rect(self.screen, C_GRAY, (bx, by, 200, 190), 1, border_radius=10)

            if idx in CAT_SPRITES:
                icon = pygame.transform.scale(CAT_SPRITES[idx], (60, 60))
                if not owned:
                    dark = pygame.Surface((60, 60), pygame.SRCALPHA)
                    dark.fill((80, 80, 80, 160))
                    icon = icon.copy()
                    icon.blit(dark, (0, 0))
                self.screen.blit(icon, (bx + 70, by + 18))
            else:
                alpha_color = cdef["color"] if owned else C_GRAY
                draw_unit_shape(self.screen, bx+100, by+48, cdef.get("shape","round"),
                                cdef["size"]//2+6, alpha_color, 1)
            draw_text(self.screen, cdef["name"],  bx+100, by+85, font_med,
                      C_WHITE if owned else C_GRAY, center=True)
            draw_text(self.screen, f"Lv {lvl}/{self.MAX_LEVEL}", bx+100, by+108,
                      font_med, C_XP if owned else C_GRAY, center=True)

            if owned:
                if cost is not None:
                    can = self.save["xp"] >= cost
                    ubg = (20,50,20) if can else (30,20,20)
                    uc  = C_GREEN if can else C_RED
                    pygame.draw.rect(self.screen, ubg,  (bx+50, by+150, 100, 30), border_radius=6)
                    pygame.draw.rect(self.screen, uc,   (bx+50, by+150, 100, 30), 2, border_radius=6)
                    draw_text(self.screen, f"UP ({cost} XP)", bx+100, by+156,
                              font_small, uc, center=True)
                else:
                    draw_text(self.screen, "MAX LEVEL", bx+100, by+140,
                              font_med, C_YELLOW, center=True)
            else:
                draw_text(self.screen, "Locked", bx+100, by+140,
                          font_small, C_GRAY, center=True)

        if self.msg_timer > 0:
            draw_text(self.screen, self.message, SW//2, SH-50, font_big, C_XP, center=True)

class StageSelectScene:
    def __init__(self, save, screen):
        self.save = save
        self.screen = screen
        self.selected = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for idx, stage in enumerate(STAGES):
                col = idx % 3
                row = idx // 3
                bx = 80 + col * 380
                by = 80 + row * 140
                if bx <= mx <= bx+340 and by <= my <= by+110:
                    unlocked = (idx == 0 or (idx-1) in self.save["stages_cleared"])
                    if unlocked:
                        self.selected = idx
                        return

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill(C_DARK)
                                            

        for idx, stage in enumerate(STAGES):
            col = idx % 3
            row = idx // 3
            bx = 80 + col * 380
            by = 80 + row * 140

            cleared  = idx in self.save["stages_cleared"]
            unlocked = (idx == 0 or (idx-1) in self.save["stages_cleared"])

            bg = (10,30,10) if cleared else ((20,20,40) if unlocked else (15,15,15))
            border = C_GREEN if cleared else (C_BLUE if unlocked else C_GRAY)

            pygame.draw.rect(self.screen, bg,     (bx, by, 340, 110), border_radius=10)
            pygame.draw.rect(self.screen, border, (bx, by, 340, 110), 2, border_radius=10)

            if idx < 3:
                icon_color = (60, 130, 230)                 
            elif idx < 7:
                icon_color = (255, 210, 40)                     
            else:
                icon_color = (220, 50, 50)                 
            pygame.draw.rect(self.screen, icon_color, (bx+10, by+10, 60, 90), border_radius=6)

            name_font = fit_font(stage["name"], 240, start_size=22)
            draw_text(self.screen, stage["name"], bx+85, by+25, name_font,
                      C_WHITE if unlocked else C_GRAY)

            status = "cleared!" if cleared else ("play" if unlocked else "locked")
            sc = C_GREEN if cleared else (C_WHITE if unlocked else C_GRAY)
            draw_text(self.screen, status, bx+85, by+65, font_med, sc)

class MenuScene:
    def __init__(self, save, screen):
        self.save = save
        self.screen = screen
        self.options = ["Play", "Shop", "Upgrades", "Quit"]
        self.hovered = -1

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            self.hovered = -1
            for i, opt in enumerate(self.options):
                bx, by = SW//2-120, 280+i*80
                if bx <= mx <= bx+240 and by <= my <= by+55:
                    self.hovered = i
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered >= 0:
                return self.hovered
        return None

    def update(self, dt):
        pass

    def draw(self, t):
        self.screen.fill((10, 15, 30))
        random.seed(42)
        for _ in range(120):
            sx = random.randint(0, SW)
            sy = random.randint(0, SH//2)
            r  = random.randint(1, 3)
            bri = int(150 + 100*math.sin(t*2 + sx*0.1))
            pygame.draw.circle(self.screen, (bri,bri,bri), (sx,sy), r)
        random.seed()

        title_y = 80 + int(math.sin(t*1.5)*6)
        draw_text(self.screen, "The Nathans vs the Aruns", SW//2, title_y, font_big,
                  C_YELLOW, center=True)

        cleared = len(self.save["stages_cleared"])
        draw_text(self.screen, f"nathan food: {self.save['cat_food']}   xp: {self.save['xp']}   stages cleared: {cleared}/{len(STAGES)}",
                  SW//2, 195, font_small, C_XP, center=True)

        for i, opt in enumerate(self.options):
            bx, by = SW//2-120, 280+i*80
            hot = (i == self.hovered)
            bg = (40,40,80) if hot else (20,20,40)
            bc = C_YELLOW if hot else C_BLUE
            pygame.draw.rect(self.screen, bg, (bx, by, 240, 55), border_radius=10)
            pygame.draw.rect(self.screen, bc, (bx, by, 240, 55), 2, border_radius=10)
            draw_text(self.screen, opt, SW//2, by+14, font_big, C_WHITE, center=True)

def main():
    screen = pygame.display.set_mode((SW, SH))
    pygame.display.set_caption("The Nathans vs the Aruns")
    load_sprites()
    clock = pygame.time.Clock()

                            
    _music_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "music.mp3")
    if _os.path.exists(_music_path):
        pygame.mixer.music.load(_music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)                     
    save  = load_save()

    scene_name = "menu"
    menu    = MenuScene(save, screen)
    shop    = None
    upgrade = None
    stages  = None
    battle  = None
    t = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        t += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if scene_name == "menu":
                result = menu.handle_event(event)
                if result == 0:
                    scene_name = "stages"
                    stages = StageSelectScene(save, screen)
                elif result == 1:
                    scene_name = "shop"
                    shop = ShopScene(save, screen)
                elif result == 2:
                    scene_name = "upgrade"
                    upgrade = UpgradeScene(save, screen)
                elif result == 3:
                    running = False

            elif scene_name == "stages":
                stages.handle_event(event)
                if stages.selected is not None:
                    battle = BattleScene(stages.selected, save, screen)
                    scene_name = "battle"
                    stages.selected = None
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    scene_name = "menu"

            elif scene_name == "battle":
                if battle.result and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    scene_name = "menu"
                    menu = MenuScene(save, screen)
                    particles.clear()
                else:
                    battle.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    scene_name = "menu"
                    particles.clear()

            elif scene_name in ("shop", "upgrade"):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    scene_name = "menu"
                if scene_name == "shop" and shop:
                    shop.handle_event(event)
                if scene_name == "upgrade" and upgrade:
                    upgrade.handle_event(event)

        if scene_name == "menu":
            menu.update(dt)
        elif scene_name == "stages":
            stages.update(dt)
        elif scene_name == "battle":
            battle.update(dt)
        elif scene_name == "shop":
            shop.update(dt)
        elif scene_name == "upgrade":
            upgrade.update(dt)

        if scene_name == "menu":
            menu.draw(t)
        elif scene_name == "stages":
            stages.draw()
            draw_text(screen, "ESC = Back", 10, SH-25, font_small, C_GRAY)
        elif scene_name == "battle":
            battle.draw()
            draw_text(screen, "ESC = Quit battle", 10, 10, font_small, C_GRAY)
        elif scene_name == "shop":
            shop.draw()
            draw_text(screen, "ESC = Back", 10, SH-25, font_small, C_GRAY)
        elif scene_name == "upgrade":
            upgrade.draw()
            draw_text(screen, "ESC = Back", 10, SH-25, font_small, C_GRAY)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()