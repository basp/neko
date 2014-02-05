import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
FONT_FLAGS = libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
FONT_FILE = 'fonts/dejavu12x12_gs_tc.png'
LIMIT_FPS = 25
TITLE = 'Neko (noise test)'

libtcod.sys_set_fps(LIMIT_FPS)
libtcod.console_set_custom_font(FONT_FILE, FONT_FLAGS)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, False)

rng = libtcod.random_new()
noise2d = libtcod.noise_new(2, random=rng)
libtcod.noise_set_type(noise2d, libtcod.NOISE_SIMPLEX)

while not libtcod.console_is_window_closed():
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_clear(0)
    for i in range(SCREEN_HEIGHT):
        for j in range(SCREEN_WIDTH):
            x, y = float(j) / SCREEN_WIDTH, float(i) / SCREEN_HEIGHT
            n = libtcod.noise_get_fbm(noise2d, [x, y], 16)
            v = int((n + 1) * 128)
            c = libtcod.Color(v, v, v)
            libtcod.console_set_char_background(0, j, i, c, libtcod.BKGND_SET)

    libtcod.console_flush()
    libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)