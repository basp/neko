import libtcodpy as libtcod
import gradient

SCREEN_WIDTH = 40
SCREEN_HEIGHT = 40

ASPECT = float(SCREEN_HEIGHT) / SCREEN_WIDTH

FONT_FILE = 'fonts/terminal12x12_gs_ro.png'
FONT_FLAGS = libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW

libtcod.console_set_custom_font(FONT_FILE, FONT_FLAGS)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Neko (world gen spike)', False)

rng = libtcod.random_new()
noise2d = libtcod.noise_new(2)
libtcod.noise_set_type(noise2d, libtcod.NOISE_SIMPLEX)

terrain = gradient.terrain()
gray = gradient.gray_scale()

def render_all(grad):
    for r in range(SCREEN_HEIGHT):
        for c in range(SCREEN_WIDTH):
            s = 1.0
            x, y = float(c) / (s * ASPECT * SCREEN_WIDTH), float(r) / (s * SCREEN_HEIGHT)
            n = libtcod.noise_get_fbm(noise2d, [x, y], 4)
            color = grad.get_color(n)
            libtcod.console_set_char_background(0, c, r, color, libtcod.BKGND_SET) 

while not libtcod.console_is_window_closed():
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_clear(0)
    render_all(terrain)
    libtcod.console_flush()
    libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
