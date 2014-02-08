# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import array
import libtcodpy as libtcod

class KeyPressEventArgs:
    def __init__(self, key):
        self.key = key
        self.handled = False

class TextArea:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.con = libtcod.console_new(w, h)
        self.fg = libtcod.Color(255, 255, 255)
        self.bg = libtcod.Color(0, 0, 0)
        self.transparency = 1.0
        self.text = array.array('c')
        self.cursor_pos = 0
        self.interval = 1600
        self.half_interval = self.interval / 2

    def _insert_char(self, c):
        """Inserts a character at cursor position."""
        cursor_x, cursor_y = self._get_cursor_coords()
        self.text.insert(self.cursor_pos, c)
        self.cursor_pos += 1

    def _delete_char(self):
        """Deletes a character at cursor position."""
        if self.cursor_pos > 0:
            self.text.pop(self.cursor_pos - 1)
            self.cursor_pos -= 1

    def _get_cursor_coords(self):
        """Converts current cursor_pos into console coordinates."""
        x = 0
        y = 0
        for i in range(self.cursor_pos):
            if self.text[i] == '\n':
                y += 1
                x = 0
            else:
                x += 1
        return x, y

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
            pass
        elif key.vk == libtcod.KEY_DOWN:
            pass
        elif key.vk == libtcod.KEY_HOME:
            self.cursor_pos = 0
        elif key.vk == libtcod.KEY_END:
            self.cursor_pos = len(self.text)
        elif key.vk == libtcod.KEY_ENTER:
            self._insert_char('\n')
        elif key.c > 31:
            self._insert_char(chr(key.c))

    def render(self, con):
        time = libtcod.sys_elapsed_milli()
        libtcod.console_set_default_foreground(self.con, self.fg)
        libtcod.console_set_default_background(self.con, self.bg)
        libtcod.console_clear(self.con)         
        x = 0
        y = 0
        for c in self.text:
            if c == '\n':
                y += 1
                x = 0
            else:
                libtcod.console_set_char(self.con, x, y, c)
                x += 1
        cursor_on = (time % self.interval) > self.half_interval       
        cursor_x, cursor_y = self._get_cursor_coords()
        if cursor_on:
            libtcod.console_set_char_foreground(self.con, cursor_x, cursor_y, self.bg)
            libtcod.console_set_char_background(self.con, cursor_x, cursor_y, self.fg, libtcod.BKGND_SET)
        else:
            libtcod.console_set_char_foreground(self.con, cursor_x, cursor_y, self.fg)
            libtcod.console_set_char_background(self.con, cursor_x, cursor_y, self.bg, libtcod.BKGND_SET)
        libtcod.console_blit(self.con, 0, 0, self.w, self.h, con, self.x, self.y, 1.0, self.transparency)