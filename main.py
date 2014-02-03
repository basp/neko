import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

FONT_FLAGS = libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
FONT_FILE = 'fonts/dejavu10x10_gs_tc.png'

TITLE = 'Neko (lost kitty)'

libtcod.console_set_custom_font(FONT_FILE, FONT_FLAGS)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, False)

def handle_keys():
    global player_x, player_y

    key = libtcod.console_wait_for_keypress(True)
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
        return True

    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player_y -= 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player_y += 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player_x -= 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player_x += 1

player_x = SCREEN_WIDTH / 2
player_y = SCREEN_HEIGHT / 2

while not libtcod.console_is_window_closed():
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_put_char(0, player_x, player_y, '@', libtcod.BKGND_NONE)
    libtcod.console_flush()
    libtcod.console_put_char(0, player_x, player_y, ' ', libtcod.BKGND_NONE)
    exit = handle_keys()
    if exit:
        break