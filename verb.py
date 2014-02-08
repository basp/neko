import unittest

def verb(names, verbargs):
    def _verb(f):
        f.__dict__['names'] = names
        f.__dict__['args'] = verbargs
        return f
    return _verb

class Foo:
    @verb('b*ar', ('any', 'any', 'any'))
    def bar(self, *args, **kwargs):
        pass

class Metadata(unittest.TestCase):
    def test_data(self):
        foo = Foo()
        self.assertTrue('names' in foo.bar.__dict__)
        self.assertTrue('args' in foo.bar.__dict__)
        self.assertEqual('b*ar', foo.bar.__dict__['names'])
        self.assertEqual(('any', 'any', 'any'), foo.bar.__dict__['args'])