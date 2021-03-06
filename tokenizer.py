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

import unittest

def tokenize(s):
    tokens = []
    s = s.strip()
    while len(s) > 0:
        s = skip_ws(s)
        w, s = word(s)
        tokens.append(w)
    return tokens

def word(s):
    r = ''
    i = 0
    while i < len(s):
        if s[i] == '"': 
            return quoted_string(s[i + 1:], r)
        if s[i] == ' ':
            return r, s[i + 1:]
        else:
            r += s[i]
        i += 1
    return r, ''

def quoted_string(s, prefix=''):
    r = prefix
    i = 0
    while i < len(s):
        if s[i:i + 2] == '" ':
            return r, s[i + 2:]
        elif s[i] != '"':
            r += s[i]
        i += 1
    return r, ''

def skip_ws(s):
    i = 0
    while i < len(s):
        if s[i] != ' ':
            return s[i:]
        i += 1
    return ''

class Tokenizing(unittest.TestCase):
    def assert_tokens(self, s, expected):
        tokens = tokenize(s)
        self.assertEqual(len(expected), len(tokens))
        for i in range(len(expected)):
            self.assertEqual(expected[i], tokens[i])

    def test_parse_words(self):
        s = 'foo "bar mumble" baz" "fro"tz" bl"o"rt'
        expected = ['foo', 'bar mumble', 'baz frotz', 'blort']
        self.assert_tokens(s, expected)

    def test_parse_words_should_strip(self):
        s = '         foo "bar mumble" baz" "fro"tz" bl"o"rt        '
        expected = ['foo', 'bar mumble', 'baz frotz', 'blort']
        self.assert_tokens(s, expected)

if __name__ == '__main__':
    unittest.main()