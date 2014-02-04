import libtcodpy as libtcod

if __name__ == '__main__':
    b, f = libtcod.Color(78, 68, 216), libtcod.Color(163, 150, 255)
    txt = libtcod.text_init(4, 4, 40, 25, 0)
    libtcod.text_set_properties(txt, 0, 800, "\nfoo\n", 4)
    libtcod.text_set_colors(txt, f, b, 1)
    inputting = True
    libtcod.console_init_root(48, 34, "Textfield test", False)
    libtcod.sys_set_fps(25)
    while not libtcod.console_is_window_closed():
        libtcod.console_set_default_background(0, f)
        libtcod.console_clear(0)
        libtcod.text_render(txt, 0)
        if not inputting:
            libtcod.text_reset(txt)
        libtcod.console_flush()
        key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
        inputting = libtcod.text_update(txt, key)
