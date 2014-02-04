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

import libtcodpy as libtcod

class View:
    def __init__(self, w, h, x=0, y=0):
        self.w = w
        self.h = h
        self.x = x
        self.y = y

class TextView:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.con = libtcod.console_new(w, h)
        self.lines = []
        self.view = View(w, h)

    def append(self, line):
        self.lines.append(line)

    def render(self, con):
        max_y = len(self.lines) - 1
        y1 = min(self.view.y, max_y)
        y2 = min(self.view.y + self.view.h, max_y)
        if y1 > y2 or y1 < 0 or y2 < 0:
            return
        flags = libtcod.BKGND_SET | libtcod.LEFT 
        y = 0
        for i in range(y1, y2 + 1):
            s = self.lines[i]
            # WTF is going on with `console_print_rect_ex'? It seems like we need to 
            # pass in double the width of our console? When we pass in self.w we only
            # get half the string... Is this a unicode thing?
            libtcod.console_print_rect_ex(self.con, 0, y, 2 * self.w, 1, flags, '%s', s)
            y += 1
        libtcod.console_blit(self.con, 0, 0, self.w, self.h, con, self.x, self.y, 1.0, 1.0)
