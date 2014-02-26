import unittest

def wrap(s, max_len):
    last_ws = 0
    for i in range(len(s)):
        if s[i] == ' ':
            last_ws = i
        if i == max_len:
            return s[:last_ws], s[last_ws + 1:]
    return s, ''

def _prop(obj, prop):
    if hasattr(obj, prop):
        return getattr(obj, prop)
    else:
        return '<%s>' % prop

def pronoun_sub(text, who=None, **kwargs):
    if len(text) <= 1: 
        return text
    for k in ['player', 'dobj', 'iobj', 'this']:
        if not k in kwargs: 
            kwargs[k] = None
    if who is None: 
        who = kwargs['player']
    output = ''
    i = 0
    while i < len(text):
        if text[i] == '%':
            code = text[i + 1]
            if code == '%':
                output += '%'
            elif code == 's':
                output += _prop(who, 'ps')
            elif code == 'o':
                output += _prop(who, 'po')
            elif code == 'p':
                output += _prop(who, 'pp')
            elif code == 'r':
                output += _prop(who, 'pr')
            elif code == 'n':
                output += _prop(who, 'name')
            elif code == 'd':
                output += _prop(kwargs['dobj'], 'name')
            elif code == 'i':
                output += _prop(kwargs['iobj'], 'name')
            elif code == 't':
                output += _prop(kwargs['this'], 'name')
            i += 1
        else:
            output += text[i]
        i += 1
    return output

class Foo:
    def __init__(self):
        self.ps = 'he'
        self.po = 'him'
        self.pp = 'his'
        self.pr = 'himself'
        self.name = 'Foo'
        self.bar = 'quux'
        self.plural = False

class TestCase(unittest.TestCase):
    def test_substition(self):
        who = Foo()
        cases = [
            ('_%s_', '_he_'),
            ('_%o_', '_him_'),
            ('_%p_', '_his_'),
            ('_%r_', '_himself_'),
            ('_%n_', '_Foo_'),
            ('_%d_', '_<name>_') ]
        for text, expected in cases:
            actual = pronoun_sub(text, who)
            self.assertEqual(actual, expected)

    def test_wrap(self):
        s = '1 3 5 7 9'
        self.assertEqual(wrap(s, 1), ('1', '3 5 7 9'))
        self.assertEqual(wrap(s, 2), ('1', '3 5 7 9'))
        self.assertEqual(wrap(s, 3), ('1 3', '5 7 9'))
        self.assertEqual(wrap(s, 4), ('1 3', '5 7 9'))

if __name__ == '__main__':
    unittest.main()