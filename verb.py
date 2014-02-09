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

def verb(names, verbargs):
    def _verb(f):
        f.__dict__['names'] = names
        f.__dict__['args'] = verbargs
        return f
    return _verb

def valid_verb(f):
    return 'names' in f.__dict__ and 'args' in f.__dict__

def verbs(obj):
    routines = inspect.getmembers(obj, lambda x: inspect.isroutine(x))
    return [f for n, f in routines if not n.startswith('__') and valid_verb(f)]

class Foo:
    def none_verb(self):
        pass

    @verb('b*ar', ('any', 'any', 'any'))
    def bar(self, *args, **kwargs):
        pass

    @verb('f*oo', ('this', 'none', 'this'))
    def foo(self, *args, **kwargs):
        pass

class Metadata(unittest.TestCase):
    def test_data(self):
        foo = Foo()
        self.assertTrue('names' in foo.bar.__dict__)
        self.assertTrue('args' in foo.bar.__dict__)
        self.assertEqual('b*ar', foo.bar.__dict__['names'])
        self.assertEqual(('any', 'any', 'any'), foo.bar.__dict__['args'])

    def test_list(self):
        foo = Foo()
        vbs = verbs(foo)
        self.assertEqual(2, len(vbs))
        self.assertEqual('b*ar', vbs[0].__dict__['names'])
        self.assertEqual(('any', 'any', 'any'), vbs[0].__dict__['args'])