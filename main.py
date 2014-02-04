import libtcodpy as libtcod
import textfield

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

FONT_FLAGS = libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
FONT_FILE = 'fonts/dejavu10x10_gs_tc.png'

LIMIT_FPS = 20

TITLE = 'Neko (lost kitty)'

libtcod.console_set_custom_font(FONT_FILE, FONT_FLAGS)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, False)

tf = textfield.TextField(1, 1, 40, 1)

while not libtcod.console_is_window_closed():
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_clear(0)
    tf.render(0)
    libtcod.console_flush()
    key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
    tf.update(key)
    if key.vk == libtcod.KEY_ENTER:
        tf.reset()