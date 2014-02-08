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

class AmbiguousMatch(Exception):
    pass

def property(this, s):
    found = None
    props = inspect.getmembers(this, lambda x: not inspect.isroutine(x))
    for p in props:
        if p[0].startswith('__'):
            continue
        if p[0].startswith(s):
            if found is None:
                found = p
            else:
                raise AmbiguousMatch()
    return found

class Foo:
    def __init__(self):
        self.bar = 'quux'
        self.baz = 'frotz'

class Matching(unittest.TestCase):
    def test_property(self):
        foo = Foo()
        self.assertEqual(('bar', 'quux'), property(foo, 'bar'))
        self.assertEqual(('baz', 'frotz'), property(foo, 'baz'))

if __name__ == '__main__':
    unittest.main()