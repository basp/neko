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
                for s in v: 
                    print(s)
            else:
                print(v)

    def moveto(self, where):
        world.move(self, where)

class Exit(Root):
    def __init__(self):
        super().__init__()
        self.other_side = None

class Actor(Root):
    def __init__(self):
        super().__init__()
        self.wielded = None

class Player(Actor):
    @verb('l*ook', ('none', 'none', 'none'))
    def look_around(self, *args, **kwargs):
        player = kwargs['player']
        if player.location:
            player.tell(player.location.map)
        else:
            print("You are nowhere.")

    @verb('l*ook', ('any', 'none', 'none'))
    def look_thing(self, *args, **kwargs):
        player, thing = kwargs['player'], kwargs['dobj']
        if thing:
            player.tell("You look at something.")
        else:
            player.tell("There is no `%s' here." % kwargs['dobjstr'])

    @verb('k*ill', ('any', 'none', 'none'))
    def kill(self, *args, **kwargs):
        if kwargs['dobj']:
            if kwargs['dobj'] == kwargs['player']:
                self.kill_myself(*args, **kwargs)
            else:
                print("You attack %s!" % kwargs['dobj'].name)
        elif kwargs['dobjstr']:
            print("There is no `%s' here." % kwargs['dobjstr'])
        else:
            print("Kill what?")

    def kill_myself(self, *args, **kwargs):
        if self.wielded:
            print("Wow you are wielding a weapon... FAileD TO CoMPUtE~")
        else:
            print("You try to strangle yourself but that doesn't really work.")

    @verb('h*elp', ('any', 'any', 'any'))
    def help(self, *args, **kwargs):
        print("You yell for help. There is no answer.")

class Room(Root):
    def __init__(self):
        super().__init__(self)
        self.area = None
        self.coords = None
        self.area_icon = Fore.GREEN + '//'
        self.map_icon = Fore.WHITE + '[]'
        self.map = []
        self.exits = []

    def _render_map_stub(self):
        self.map = [
            self.area_icon * 5,
            self.area_icon * 5,
            self.area_icon * 2 + Fore.BLUE + '()' + self.area_icon * 2,
            self.area_icon * 5,
            self.area_icon * 5 ]

class Area(Root):
    pass

def generate_map(area):
    levels = {}
    mapped_room = lambda x: hasattr(x, 'coords') and x.coords
    rooms = [x for x in area.contents if mapped_room]
    for r in rooms:
        x, y, z = r.coords
        if not z in levels: levels[z] = []
        levels[z].append(r)
    for z in levels:
        max_x, max_y = 0, 0
        for r in levels[z]:
            x, y, z = r.coords
            if x > max_x: max_x = x
            if y > max_y: max_y = y
        print(levels[z])


def parse(player, s):
    tokens = tokenizer.tokenize(s)
    cmd = command.parse(tokens)
    return world.resolve(player, cmd)

def exec(cmd, player):
    if callable(cmd['f']):
        args = cmd['args']
        cmd.update({'player': player}) 
        cmd['f'](args, **cmd)    

def prompt():
    return Style.BRIGHT + Fore.CYAN + "> " + Style.RESET_ALL

foo = Root()
foo.name = 'foo'
player = Player()
player.is_player = True
player.wielded = 'fubar'
room = Room()
room.coords = (0, 0, 0)
room._render_map_stub()
world.move(player, room)
world.move(foo, room)
area = Area()
world.move(room, area)

def syntax_highlighting_stub(s):
    s = str(s)
    s = s.replace(':', Style.BRIGHT + Fore.YELLOW + ':' + Style.RESET_ALL)
    s = s.replace('{', Style.BRIGHT + Fore.CYAN + '{' + Style.RESET_ALL)
    s = s.replace('}', Style.BRIGHT + Fore.CYAN + '}' + Style.RESET_ALL)
    return s

def loop():
    while True:
        s = input(prompt())
        cmd = parse(player, s)
        print(syntax_highlighting_stub(cmd))
        if cmd['verb'] == '@quit': 
            break
        exec(cmd, player)        

if __name__ == '__main__':
    loop()