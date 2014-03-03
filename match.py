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
    s = s.lower()
    for o in objects:
        if not hasattr(o, 'names'): continue
        if not callable(o.names): continue
        for n in o.names():
            if n.lower().startswith(s):
                if found is None:
                    found = o
                    break
                else:
                    return Ambiguous
    return found

def verb(s, v):
    # filter out empty entries
    chunks = list(filter(None, v.split('*')))
    if len(chunks) == 2:
        return str.join('', chunks).startswith(s)
    elif v.endswith('*'):
        return s.startswith(chunks[0])
    else:
        return s == v

def _match_obj_arg(this, obj, objstr, arg):
    if arg == 'none':
        return obj is None and objstr == ''
    elif arg == 'this':
        return obj == this
    elif arg == 'any':
        return True
    else:
        return False

def _match_pred_arg(prep, arg):
    if arg == 'none':
        return prep == ''
    elif arg == 'any':
        return True
    else:
        preps = [x.strip() for x in arg.split(',')]
        return prep in set(preps)

def verbargs(this, args, cmd):
    dobj, dobjstr = cmd['dobj'], cmd['dobjstr']
    iobj, iobjstr = cmd['iobj'], cmd['iobjstr']
    prep = cmd['prepstr']
    dobj_arg, prep_arg, iobj_arg = args
    result = _match_obj_arg(this, dobj, dobjstr, dobj_arg)
    result = result and _match_obj_arg(this, iobj, iobjstr, iobj_arg)
    result = result and _match_pred_arg(prep, prep_arg)
    return result

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

    def test_verb(self):
        self.assertTrue(verb('foo', 'foo'))
        self.assertTrue(verb('foo', 'foo*'))
        self.assertTrue(verb('fooq', 'foo*'))
        self.assertTrue(verb('foo', 'foo*bar'))
        self.assertFalse(verb('quux', 'foo*bar'))
        self.assertFalse(verb('fooq', 'foo*bar'))
        self.assertTrue(verb('fooba', 'foo*bar'))

    def test_verbargs(self):
        args = ('none', 'none', 'none')
        cmd = {'dobj': None, 'prepstr': '', 'iobj': None}
        self.assertTrue(verbargs(None, args, cmd))
        foo = Foo('baz')
        bar = Foo('bar')
        cmd['dobj'] = foo
        self.assertFalse(verbargs(None, args, cmd))
        args = ('this', 'none', 'none')
        self.assertTrue(verbargs(foo, args, cmd))
        cmd['dobj'] = None
        args = ('any', 'any', 'any')
        self.assertTrue(verbargs(None, args, cmd))
        args = ('this', 'with, using', 'any')
        cmd['dobj'] = foo
        cmd['prepstr'] = 'using'
        cmd['iobj'] = bar
        self.assertTrue(verbargs(foo, args, cmd))
        cmd['prepstr'] = 'quux'
        self.assertFalse(verbargs(foo, args, cmd))
        cmd['prepstr'] = 'with'
        self.assertTrue(verbargs(foo, args, cmd))

if __name__ == '__main__':
    unittest.main()