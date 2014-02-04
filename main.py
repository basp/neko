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
import tokenizer
import match
import textfield
import textview

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 35
FONT_FLAGS = libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
FONT_FILE = 'fonts/dejavu12x12_gs_tc.png'
LIMIT_FPS = 25
TITLE = 'Neko (lost kitty)'

text_field = textfield.TextField(0, SCREEN_HEIGHT - 1, SCREEN_WIDTH, 1)
text_view = textview.TextView(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - 1)
builtins = {'me': 123} # $tags: stub, example, todo

def eval_str(s, globals):
    try:
        r = eval(s, globals)
        return str(r)
    except Exception as e:
        return str(e)

def on_command(sender, args):
    if args.key.vk != libtcod.KEY_ENTER:
        return
    s = text_field.get_text()
    if match.starts_with(';', s):
        r = eval_str(s[1:], builtins)
        text_view.lines.append(str(r))
    else:
        tokens = tokenizer.tokenize(s)
        text_view.lines.append(str(tokens))

text_field.add_handler(on_command)
libtcod.sys_set_fps(LIMIT_FPS)
libtcod.console_set_custom_font(FONT_FILE, FONT_FLAGS)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, False)

while not libtcod.console_is_window_closed():
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_clear(0)
    text_field.render(0)
    text_view.render(0)
    libtcod.console_flush()
    key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
    text_field.update(key)