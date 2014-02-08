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

ESC = chr(27)

def _e(n):
    return ESC + "[%im" % n

class Style:
    RESET_ALL   = _e(0)
    BRIGHT      = _e(1)
    DIM         = _e(2)
    NORMAL      = _e(22)

class Fore:
    BLACK       = _e(30)
    RED         = _e(31)
    GREEN       = _e(32)
    YELLOW      = _e(33)
    BLUE        = _e(34)
    MAGENTA     = _e(35)
    CYAN        = _e(36)
    WHITE       = _e(37)
    RESET       = _e(39) 

class Back:
    BLACK       = _e(40)
    RED         = _e(41)
    GREEN       = _e(42)
    YELLOW      = _e(43)
    BLUE        = _e(44)
    MAGENTA     = _e(45)
    CYAN        = _e(46)
    WHITE       = _e(47)
    RESET       = _e(49) 