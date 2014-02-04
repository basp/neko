import array
import libtcodpy as libtcod

class KeyPressEventArgs:
    def __init__(self, key):
        self.key = key
        self.handled = False

class TextField:
    def __init__(self, x, y, w, h, handlers=[], prompt='', max_history=100):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.con = libtcod.console_new(w, h)
        self.fg = libtcod.Color(255, 255, 255)
        self.bg = libtcod.Color(0, 0, 0)
        self.transparency = 1.0
        self.prompt = prompt
        self.text = array.array('c')
        self.text_x = len(prompt)
        self.text_y = 0
        self.cursor_pos = 0
        self.interval = 800
        self.half_interval = self.interval / 2
        self.handlers = handlers
        self.max_history = max_history
        self.history = []
        self.history_i = -1

    def _insert_char(self, c):
        """Inserts a character at cursor position."""
        if self.cursor_pos < self.w - 1:
            self.text.insert(self.cursor_pos, c)
            self.cursor_pos += 1

    def _delete_char(self):
        """Deletes a character at cursor position."""
        if self.cursor_pos > 0:
            self.text.pop(self.cursor_pos - 1)
            self.cursor_pos -= 1

    def _get_cursor_coords(self):
        """Converts current cursor_pos into console coordinates."""
        x = self.text_x + self.cursor_pos
        y = 0
        return x, y

    def _update_history(self, text):
        """Updates internal command history."""
        if len(self.history) > 0:
            if text != self.history[0]:
                self.history.insert(0, text)
        else:
            self.history.insert(0, text)
        # Exceeding history length, remove the oldest item
        if len(self.history) > self.max_history:
            self.history.pop()       

    def add_handler(self, h):
        self.handlers.append(h)
        return h

    def get_text(self):
        return self.text.tostring()

    def set_text(self, v):
        self.text = array.array('c', v)
        self.cursor_pos = len(self.text)

    def reset(self):
        self.history_i = -1
        self.cursor_pos = 0
        self.text = array.array('c')

    def update(self, key):
        args = KeyPressEventArgs(key)
        if not key.pressed:
            return
        for h in self.handlers:
            h(self, args)
        if args.handled:
            return
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
        elif key.vk == libtcod.KEY_UP:
            if self.history_i < len(self.history) - 1:
                self.history_i += 1
                self.set_text(self.history[self.history_i])
        elif key.vk == libtcod.KEY_DOWN:
            if self.history_i > 0:
                self.history_i -= 1
                self.set_text(self.history[self.history_i])
        elif key.vk == libtcod.KEY_HOME:
            self.cursor_pos = 0
        elif key.vk == libtcod.KEY_END:
            self.cursor_pos = len(self.text)
        elif key.vk == libtcod.KEY_ENTER:
            t = self.get_text()
            self._update_history(t)
            self.reset()
        elif key.c > 31:
            self._insert_char(chr(key.c))

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
        cursor_on = (time % self.interval) > self.half_interval       
        cursor_x, cursor_y = self._get_cursor_coords()
        if cursor_on:
            libtcod.console_set_char_foreground(self.con, cursor_x, cursor_y, self.bg)
            libtcod.console_set_char_background(self.con, cursor_x, cursor_y, self.fg, libtcod.BKGND_SET)
        else:
            libtcod.console_set_char_foreground(self.con, cursor_x, cursor_y, self.fg)
            libtcod.console_set_char_background(self.con, cursor_x, cursor_y, self.bg, libtcod.BKGND_SET)
        libtcod.console_blit(self.con, 0, 0, self.w, self.h, con, self.x, self.y, 1.0, self.transparency)