import unittest

#   Code    Prop        Pronoun         Defaults
#   ---------------------------------------------------------
#   %%                                  %
#   %s      who.ps      subjective      he, she, it
#   %o      who.po      objectvie       him, her, it
#   %p      who.pp      possessive      his, her, its
#   %r      who.pr      reflexive       himself, herself, itself
#
#   %n      who.name    
#   %d      dobj.name
#   %i      iobj.name
#   %t      this.name
#   %(xyz)  who.xyz
#

def ps(text, who=None, **kwargs):
    if len(text) <= 1: 
        return text
    if who is None: 
        who = kwargs['player']
    output = ''
    for i in range(len(text)):
        if text[i] == '%':
            code = text[i + 1]
            if code == '%':
                output += '%'
            elif code == 's':
                output += who.ps
            elif code == 'o':
                output += who.po
            elif code == 'p':
                output += who.pp
            elif code == 'r':
                output += who.pr
            elif code == 'n':
                output += who.name
            elif code == 'd':
                output += kwargs['dobj'].name
            elif code == 'i':
                output += kwargs['iobj'].name
            elif code == 't':
                output += kwargs['this'].name
        else:
            output += text[i]
    return output

class Foo:
    def __init__(self):
        self.ps = 'he'
        self.po = 'him'
        self.pp = 'his'
        self.pr = 'himself'
        self.name = 'Foo'
        self.bar = 'quux'

class TestCase(unittest.TestCase):
    def test_subjective(self):
        pass

if __name__ == '__main__':
    unittest.main()