import tokenizer
import command

from ansi import Style, Fore, Back

class Object:
    def __init__(self):
        self.name = ''
        self.location = None
        self.contents = []

class Player(Object):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def look(self):
        print("You look around.")

def parse(s):
    tokens = tokenizer.tokenize(s)
    return command.parse(tokens)

def prompt():
    return Style.BRIGHT + Fore.CYAN + "> " + Style.RESET_ALL

def lookup_verb(obj, verb):
    if hasattr(obj, verb):
        return getattr(obj, verb)

player = Player('foo')

if __name__ == '__main__':
    while True:
        s = input(prompt())
        cmd = parse(s)
        verb = cmd['verb']
        if verb == '@quit': 
            break    
        f = lookup_verb(player, verb)
        if callable(f):
            f()
        else:
            print(cmd)