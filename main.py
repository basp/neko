import libtcodpy as libtcod
import textfield
import core

SCREEN_WIDTH = 50
SCREEN_HEIGHT = 30

FONT_FLAGS = libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
FONT_FILE = 'fonts/dejavu12x12_gs_tc.png'

LIMIT_FPS = 20

TITLE = 'Neko (lost kitty)'

libtcod.console_set_custom_font(FONT_FILE, FONT_FLAGS)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, False)

run = True

def command_handler(s):
    global run
    words = core.parse_words(s)
    print words
    if len(words) > 0:
        if words[0] == '@quit':
            run = False

tf = textfield.TextField(1, SCREEN_HEIGHT - 2, SCREEN_WIDTH - 2, 1,
    handler=command_handler)

while not libtcod.console_is_window_closed() and run:
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_clear(0)
    tf.render(0)
    libtcod.console_flush()
    key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
    tf.update(key)