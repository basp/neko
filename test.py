import tokenizer
import command

from ansi import Style, Fore, Back

def parse(s):
    tokens = tokenizer.tokenize(s)
    return command.parse(tokens)

def prompt():
    return Style.BRIGHT + Fore.CYAN + "> " + Style.RESET_ALL

class Player:
    def __init__(self):
        self.name = ''

if __name__ == '__main__':
    while True:
        s = input(prompt())
        cmd = parse(s)
        if cmd['verb'] == '@quit': break        
        print(cmd)