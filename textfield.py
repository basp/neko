import array
import libtcodpy as libtcod

class TextField:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.con = libtcod.console_new(w, h)
        self.fg = libtcod.Color(255, 255, 255)
        self.bg = libtcod.Color(0, 0, 0)
        self.transparency = 1.0
        self.prompt = ''
        self.text = array.array('c')
        self.text_x = 0
        self.text_y = 0
        self.cursor_pos = 0

    def prompt(self, v=None):
        if v != None:
            self.prompt = v
            self.text_x = len(self.prompt)
        return self.prompt

    def _insert_char(self, c):
        """Inserts a character at cursor position."""
        self.text.insert(self.cursor_pos, c)
        self.cursor_pos += 1

    def _delete_char(self):
        """Deletes a character at cursor position."""
        if self.cursor_pos > 0:
            self.text.pop(self.cursor_pos - 1)
            self.cursor_pos -= 1

    def _get_cursor_coords(self):
        """Convers current cursor_pos into console coordinates."""
        x = self.text_x + self.cursor_pos
        y = 0
        return x, y

    def update(self, key):
        if key.vk == libtcod.KEY_BACKSPACE:
            self._delete_char()
        elif key.vk == libtcod.KEY_DELETE:
            if self.cursor_pos < len(self.text):
                self.cursor_pos += 1
                self._delete_char()
        elif key.vk == libtcod.KEY_LEFT:
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
        elif key.vk == libtcod.KEY_RIGHT:
            if self.cursor_pos < len(self.text):
                self.cursor_pos += 1
        elif key.c > 31:
            self._insert_char(chr(key.c))

    def reset(self):
        self.cursor_pos = 0
        self.text = array.array('c')

    def render(self, con):
        time = libtcod.sys_elapsed_milli()

        libtcod.console_set_default_foreground(self.con, self.fg)
        libtcod.console_set_default_background(self.con, self.bg)
        libtcod.console_clear(self.con)       
        
        flags = libtcod.BKGND_SET | libtcod.LEFT 
        libtcod.console_print_rect_ex(self.con, 0, 0, self.w, self.h, flags, '%s', self.prompt)
        
        cur_x = self.text_x
        for c in self.text:
            libtcod.console_set_char(self.con, cur_x, 0, c)
            cur_x += 1
        
        cursor_on = (time % 800) > 400       
        cursor_x, cursor_y = self._get_cursor_coords()
        if cursor_on:
            libtcod.console_set_char_foreground(self.con, cursor_x, cursor_y, self.bg)
            libtcod.console_set_char_background(self.con, cursor_x, cursor_y, self.fg, libtcod.BKGND_SET)
        else:
            libtcod.console_set_char_foreground(self.con, cursor_x, cursor_y, self.fg)
            libtcod.console_set_char_background(self.con, cursor_x, cursor_y, self.bg, libtcod.BKGND_SET)
        
        libtcod.console_blit(self.con, 0, 0, self.w, self.h, con, self.x, self.y, 1.0, self.transparency)