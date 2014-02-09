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

class Player(world.Object):
    @verb('l*ook', ('none', 'none', 'none'))
    def look(self, *args, **kwargs):
        print("You look around.")

    @verb('l*ook', ('any', 'none', 'none'))
    def look_dobj(self, *args, **kwargs):
        print("You look at something.")

class Room(world.Object):
    pass

player = Player()
room = Room()
player.move(room)

if __name__ == '__main__':
    while True:
        s = input(prompt())
        cmd = parse(player, s)
        verb = cmd['verb']
        if verb == '@quit': break    
        print(cmd)
        if callable(cmd['f']): cmd['f']()