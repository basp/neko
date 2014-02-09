import tokenizer
import command
import world

from verb import verb
from ansi import Style, Fore, Back

def parse(player, s):
    tokens = tokenizer.tokenize(s)
    cmd = command.parse(tokens)
    return command.resolve(player, cmd)

def prompt():
    return Style.BRIGHT + Fore.CYAN + "> " + Style.RESET_ALL

class Player(world.Object):
    @verb('l*ook', ('any', 'any', 'any'))
    def look(self, *args, **kwargs):
        print("You look around.")

player = Player()

if __name__ == '__main__':
    while True:
        s = input(prompt())
        cmd = parse(player, s)
        verb = cmd['verb']
        if verb == '@quit': break    
        print(cmd)
        if callable(cmd['f']): cmd['f']()