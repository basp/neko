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
import string_utils

from verb import verb
from ansi import Style, Fore, Back

MAX_COLS = 110

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
            # player.tell(player.location.map)
            d = player.location.format_description()
            player.tell(d)
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
        self.area_icon = Fore.WHITE + '. ' + Style.RESET_ALL
        self.map_icon = Fore.WHITE + Style.BRIGHT + '[]' + Style.RESET_ALL
        self.map = []
        self.exits = []

    def format_description(self):
        lines = []
        rest = self.description
        for l in self.map:
            max_len = MAX_COLS - (6 * 2)
            if len(rest) > 0:
                s, rest = string_utils.wrap(rest, max_len)
                lines.append(l + '  ' + s)
            else:
                lines.append(l)
        return lines

class Area(Root):
    def _gen_z_level_maps(self, level):
        level_map = [[None for y in range(64)] for x in range(64)]
        for room in level:
            x, y, _ = room.coords
            level_map[y][x] = room
        for room in level:
            rx, ry, _ = room.coords
            m = [[] for _ in range(5)]
            for row in range(5):
                for col in range(5):
                    y = ry + row - 2
                    x = rx + col - 2
                    m[row].append(room.area_icon)
                    if x >= 0 and y >= 0 and level_map[y][x]:
                        m[row][col] = level_map[y][x].map_icon
            room.map = [''.join(xs) for xs in m]

    def generate_maps(self):
        levels = {}
        mapped_room = lambda x: hasattr(x, 'coords') and x.coords
        rooms = [x for x in self.contents if mapped_room]
        for r in rooms:
            x, y, z = r.coords
            if not z in levels: levels[z] = []
            levels[z].append(r)
        for z in levels:
            self._gen_z_level_maps(levels[z])

def parse(player, s):
    tokens = tokenizer.tokenize(s)
    cmd = command.parse(tokens)
    return world.resolve(player, cmd)

def execute(cmd, player):
    if callable(cmd['f']):
        args = cmd['args']
        cmd.update({'player': player}) 
        cmd['f'](args, **cmd)    

def prompt():
    return Style.BRIGHT + Fore.CYAN + "> " + Style.RESET_ALL

def loop():
    while True:
        s = input(prompt())
        cmd = parse(player, s)
        print(cmd)
        if cmd['verb'] == '@quit': 
            break
        execute(cmd, player)        

foo = Root()
foo.name = 'foo'

player = Player()
player.is_player = True
player.wielded = 'fubar'

area = Area()

room = Room()
room.coords = (10, 10, 0)
world.move(room, area)
world.move(foo, room)

room = Room()
room.coords = (11, 10, 0)
room.map_icon = Back.BLUE + Fore.YELLOW + Style.BRIGHT + 'Va' + Style.RESET_ALL
world.move(room, area)

room = Room()
room.coords = (11, 11, 0)
room.name = 'Destroyed Building'
room.description = 'The foundation and a few walls remain but otherwise this building is completely destroyed. You might still find something of value if you look hard enough though.'
world.move(room, area)
world.move(player, room)

room = Room()
room.coords = (9, 9, 0)
room.map_icon = Fore.YELLOW + '##'
world.move(room, area)

room = Room()
room.coords = (10, 9, 0)
room.map_icon = Fore.YELLOW + '=='
world.move(room, area)

room = Room()
room.coords = (11, 9, 0)
room.map_icon = Fore.YELLOW + '=='
world.move(room, area)

room = Room()
room.coords = (12, 9, 0)
room.map_icon = Fore.YELLOW + '=='
world.move(room, area)

room = Room()
room.coords = (9, 10, 0)
room.map_icon = Fore.YELLOW + '||'
world.move(room, area)

room = Room()
room.coords = (9, 11, 0)
room.map_icon = Fore.YELLOW + '||'
world.move(room, area)

room = Room()
room.coords = (9, 12, 0)
room.map_icon = Fore.YELLOW + '||'
world.move(room, area)

area.generate_maps()

if __name__ == '__main__':
    loop()