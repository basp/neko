import string
import unittest

def parse_words(s):
    words = []
    s = string.strip(s)
    while len(s) > 0:
        s = skip_ws(s)
        w, s = word(s)
        words.append(w)
    return words

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

class CommandParsing(unittest.TestCase):
    def assert_parse_words(self, s, expected):
        words = parse_words(s)
        self.assertEqual(len(expected), len(words))
        for i in range(len(expected)):
            self.assertEqual(expected[i], words[i])

    def test_parse_words(self):
        s = 'foo "bar mumble" baz" "fro"tz" bl"o"rt'
        expected = ['foo', 'bar mumble', 'baz frotz', 'blort']
        self.assert_parse_words(s, expected)

    def test_parse_words_should_strip(self):
        s = '         foo "bar mumble" baz" "fro"tz" bl"o"rt        '
        expected = ['foo', 'bar mumble', 'baz frotz', 'blort']
        self.assert_parse_words(s, expected)

if __name__ == '__main__':
    unittest.main()