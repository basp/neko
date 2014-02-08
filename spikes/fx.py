import random
import libtcodpy as libtcod
import gradient

MAX_AGE = 80

SCREEN_WIDTH = 40
SCREEN_HEIGHT = 40

FONT_FILE = 'fonts/terminal12x12_gs_ro.png'
FONT_FLAGS = libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW

LIMIT_FPS = 60

pal = [0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,
0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,
0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,0xFFF9F7D4,
0xFFF9F7D4,0xFFF9F6B6,0xFFF8F48E,0xFFF8F364,0xFFF8F139,0xFFF9EC14,0xFFFAD51B,0xFFFCBE22,
0xFFFDA52A,0xFFFF8C31,0xFFFA802E,0xFFF4752A,0xFFEE6A26,0xFFE95E22,0xFFE3531D,0xFFDE471A,
0xFFD53613,0xFFCC250D,0xFFC31207,0xFFBB0100,0xFFAC0000,0xFF9D0000,0xFF8E0000,0xFF7F0000,
0xFF700000,0xFF610000,0xFF5A0000,0xFF550000,0xFF510000,0xFF4D0000,0xFF480000,0xFF440000,
0xFF3F0000,0xFF3B0000,0xFF370000,0xFF320000,0xFF2E0000,0xFF2A0000,0xFF250000,0xFF210000,
0xFF1C0000,0xFF180000,0xFF130000,0xFF100000,0xFF0B0000,0xFF070000,0xFF020000,0xFF000000,
0xFF000000,0xFF000000,0xFF000000,0xFF000000,0xFF000000,0xFF000000,0xFF000000,0xFF000000]

libtcod.console_set_custom_font(FONT_FILE, FONT_FLAGS)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Neko (fx spike)', False)
libtcod.sys_set_fps(LIMIT_FPS)

con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

rng = libtcod.random_new()
noise2d = libtcod.noise_new(2, random=rng)
libtcod.noise_set_type(noise2d, libtcod.NOISE_SIMPLEX)

fire = [[ 0 
    for y in range(SCREEN_HEIGHT)]
        for x in range(SCREEN_WIDTH)]

coolmap = [[ 10
    for y in range(SCREEN_HEIGHT)]
        for x in range(SCREEN_WIDTH)]

def smooth(arr, x, y):
    cnt = 0

    v = arr[x][y]
    cnt += 1

    if x < SCREEN_WIDTH - 1:
        v += arr[x + 1][y]
        cnt +=1
    if x > 0:
        v += arr[x - 1][y]
        cnt +=1
    if y < SCREEN_HEIGHT - 1:
        v += arr[x][y + 1]
        cnt +=1
    if y > 0:
        v += arr[x][y - 1]
        cnt +=1
    
    v = v / cnt

    return v

def move_particles():
    for x in range(SCREEN_WIDTH):
        for y in range(1, SCREEN_HEIGHT):
            age = smooth(fire, x, y)
            x2 = random.randint(-1, 1) + x
            if x2 < 0: 
                x2 = SCREEN_WIDTH - 1
            if x2 > SCREEN_WIDTH - 1:
                x2 = 0
            age += coolmap[x2][y - 1] + 1
            if age < 0:
                age = MAX_AGE
            if age > MAX_AGE - 1:
                age = MAX_AGE - 1
            fire[x][y - 1] = age

def add_particles():
    for x in range(SCREEN_WIDTH):
        fire[x][SCREEN_HEIGHT - 1] = random.randint(0, 20)

def create_cool_map():
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            coolmap[x][y] = random.randint(-10, 10)

    for j in range(1, 10):
        for x in range(1, SCREEN_WIDTH - 2):
            for y in range(1, SCREEN_HEIGHT - 2):
                coolmap[x][y] = smooth(coolmap, x, y)

while not libtcod.console_is_window_closed():
    move_particles()
    add_particles()
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            if fire[x][y] < MAX_AGE:
                age = smooth(fire, x, y)
                age += 10
                if age > MAX_AGE:
                    age = MAX_AGE
                col = pal[age - 1]
                libtcod.console_set_char_background(con, x, y, col, libtcod.BKGND_SET)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()
    libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)