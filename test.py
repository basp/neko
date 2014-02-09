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

import tokenizer
import command
import world

from verb import verb
from ansi import Style, Fore, Back

def parse(player, s):
    tokens = tokenizer.tokenize(s)
    cmd = command.parse(tokens)
    return world.resolve(player, cmd)

def prompt():
    return Style.BRIGHT + Fore.CYAN + "> " + Style.RESET_ALL

class Root(world.Object):
    def description(self):
        return self.description

    def describe(self, v):
        self.description = v

    def look_self(self):
        return self.description()

    def tell(self, v):
        if self.is_player:
            if type(v) is list:
                for s in v: print(s)
            else:
                print(v)

    def moveto(self, where):
        move(self, where)

class Player(Root):
    @verb('l*ook', ('any', 'any', 'any'))
    def look(self, *args, **kwargs):
        print("You look around.")

class Room(Root):
    pass

foo = Root()
foo.name = 'foo'
player = Player()
room = Room()
world.move(player, room)
world.move(foo, room)

if __name__ == '__main__':
    while True:
        s = input(prompt())
        cmd = parse(player, s)
        verb = cmd['verb']
        if verb == '@quit': break    
        print(cmd)
        if callable(cmd['f']): cmd['f']()