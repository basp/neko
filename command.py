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

PREPOSITIONS = {
    'with',
    'using',
    'at',
    # ...
}

def parse(tokens):
    args = tokens[1:]
    dobjstr, prepstr, iobjstr = parse_args(args)
    return {
        'verb'      : tokens[0], 
        'args'      : args, 
        'argstr'    : str.join(' ', args),
        'dobjstr'   : dobjstr,
        'prepstr'   : prepstr,
        'iobjstr'   : iobjstr
    }

def parse_args(tokens):
    count = len(tokens)
    for i in range(count):
        maybe_prep0 = tokens[i]
        
        if i < count - 1:
            maybe_prep1 = str.join(' ', [maybe_prep0, tokens[i + 1]])
        else:
            maybe_prep1 = None
        
        if i < count - 2:
            maybe_prep2 = str.join(' ', [maybe_prep1, tokens[i + 2]])
        else:
            maybe_prep2 = None

        if maybe_prep2 in PREPOSITIONS:
            return str.join(' ', tokens[0:i]), maybe_prep2, str.join(' ', tokens[i + 3:])
        elif maybe_prep1 in PREPOSITIONS:
            return str.join(' ', tokens[0:i]), maybe_prep1, str.join(' ', tokens[i + 2:])
        elif maybe_prep0 in PREPOSITIONS:
            return str.join(' ', tokens[0:i]), maybe_prep0, str.join(' ', tokens[i + 1:])
    
    return str.join(' ', tokens), '', ''
        
class Parsing(unittest.TestCase):
    def test_parse_verb(self):
        cmd = parse(['foo'])
        self.assertEqual('foo', cmd['verb'])

    def test_parse_args(self):
        cmd = parse(['foo', 'bar', 'quux'])
        self.assertEqual('bar quux', cmd['argstr'])
        self.assertEqual(['bar', 'quux'], cmd['args'])

    def test_parse_dobj(self):
        cmd = parse(['foo', 'bar', 'quux'])
        self.assertEqual('bar quux', cmd['dobjstr'])

    def test_parse_iobj(self):
        cmd = parse(['foo', 'bar', 'quux', 'with', 'zoz', 'nix'])
        self.assertEqual('bar quux', cmd['dobjstr'])
        self.assertEqual('zoz nix', cmd['iobjstr'])
        self.assertEqual('with', cmd['prepstr'])

if __name__ == '__main__':
    unittest.main()
