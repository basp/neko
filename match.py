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

import inspect
import unittest

class Ambiguous:
    pass

def object(s, objects):
    found = None
    if not s: return found
    for o in objects:
        if not hasattr(o, 'names'): continue
        if not callable(o.names): continue
        for n in o.names():
            if n.startswith(s):
                if found is None:
                    found = o
                else:
                    return Ambiguous
    return found

class Foo:
    def __init__(self, name, aliases=[]):
        self.name = name
        self.aliases = aliases

    def names(self):
        return [self.name] + self.aliases

class Matching(unittest.TestCase):
    def test_object(self):
        bar = Foo('bar')
        baz = Foo('baz')
        objs = [bar, baz] 
        self.assertEqual(bar, object('bar', objs))
        self.assertEqual(baz, object('baz', objs))
        self.assertIs(object('ba', objs), Ambiguous)

if __name__ == '__main__':
    unittest.main()