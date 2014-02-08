import tokenizer
import command

from ansi import Style, Fore, Back

class Object:
    def __init__(self, name=''):
        self.name = name
        self.location = None
        self.contents = []

    def names(self):
        return [self.name]

    def title(self):
        return "a " + self.name

class Player(Object):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def title(self):
        return self.name

    def look(self, **kwargs):
        dobj = kwargs['dobj']
        if dobj:
            print("You look at " + dobj.title())
        else:
            print("You look around.")

def parse(player, s):
    tokens = tokenizer.tokenize(s)
    cmd = command.parse(tokens)
    return command.resolve(player, cmd)

def prompt():
    return Style.BRIGHT + Fore.CYAN + "> " + Style.RESET_ALL

def lookup_verb(obj, verb):
    if hasattr(obj, verb):
        return getattr(obj, verb)

def move(what, where):
    where.contents.append(what)
    what.location = where

foo = Object('foo')
bar = Object('bar')
baz = Object('baz')
quux = Object('quux')
room = Object('void')
player = Player('player')

move(bar, player)
move(baz, player)
move(quux, room)
move(foo, room)
move(player, room)

if __name__ == '__main__':
    while True:
        s = input(prompt())
        cmd = parse(player, s)
        verb = cmd['verb']
        if verb == '@quit': break    
        f = lookup_verb(player, verb)
        if callable(f(**cmd)): f()