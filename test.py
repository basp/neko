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
import match

from verb import verb
from ansi import Style, Fore, Back

DEFAULT_DEBUG = False
MIN_WRAP = 40
DEFAULT_WRAP = 80

class Root(world.Object):
    def __init__(self):
        super().__init__()
        self.description = 'Nothing out of the ordinary.'

    def look_self(self, *args, **kwargs):
        return self.description

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

    def invoke(self, what, *args, **kwargs):
        if self.other_side:
            what.moveto(self.other_side)

    def look_self(self, *args, **kwargs):
        if self.other_side:
            return self.other_side.render(**kwargs)

class Actor(Root):
    def __init__(self):
        super().__init__()
        self.wielded = None

class Player(Actor):
    def __init__(self):
        super().__init__()
        self.debug = DEFAULT_DEBUG
        self.wrap = DEFAULT_WRAP

    @verb('@wrap', ('any', 'none', 'none'))
    def set_wrap(self, *args, **kwargs):
        dobjstr = kwargs['dobjstr']
        if dobjstr and dobjstr.isnumeric():
            v = int(dobjstr)
            if v < MIN_WRAP:
                self.tell('Minimum wrap is %i characters.' % MIN_WRAP)
            else:
                self.wrap = v
                self.tell('Wrap set to %i characters.' % self.wrap)

    @verb('@debug', ('any', 'none', 'none'))
    def set_debug(self, *args, **kwargs):
        dobjstr = kwargs['dobjstr']
        if dobjstr == 'on':
            self.debug = True
            self.tell('Debug output is on')
        elif dobjstr == 'off':
            self.debug = False
            self.tell('Debug output is off.')

    @verb('l*ook', ('none', 'none', 'none'))
    def look_around(self, *args, **kwargs):
        if self.location:
            d = self.location.render(*args, **kwargs)
            d.append('')
            d.append(self.location.render_exits())
            self.tell(d)
        else:
            self.tell("You are nowhere.")

    @verb('l*ook', ('any', 'none', 'none'))
    def look_thing(self, *args, **kwargs):
        player, thing = kwargs['player'], kwargs['dobj']
        if thing:
            player.tell(thing.look_self(*args, **kwargs))
        else:
            player.tell("There is no `%s' here." % kwargs['dobjstr'])

    @verb('u*p d*own e*ast w*est n*orth s*outh ne northe*ast nw northw*est se southe*ast sw southw*est', ('none', 'none', 'none'))
    def go_direction(self, *args, **kwargs):
        kwargs['dobjstr'] = kwargs['verb']
        self.go(self, *args, **kwargs)

    @verb('g*o', ('any', 'none', 'none'))
    def go(self, *args, **kwargs):
        dobjstr = kwargs['dobjstr']
        exit = match.object(dobjstr, self.location.exits)
        if exit is match.Ambiguous:
            player.tell("I'm not sure which way `%s' you mean." % dobjstr)
        elif exit:
            exit.invoke(self, *args, **kwargs)
            player.look_around(*args, **kwargs)
        else:
            player.tell("You can't go that way.")

    @verb('k*ill', ('any', 'none', 'none'))
    def kill(self, *args, **kwargs):
        player, dobj, dobjstr = kwargs['player'], kwargs['dobj'], kwargs['dobjstr']
        if dobj:
            if dobj == player:
                self.kill_myself(*args, **kwargs)
            else:
                player.tell("You attack %s!" % dobj.name)
        elif kwargs['dobjstr']:
            player.tell("There is no `%s' here." % dobjstr)
        else:
            player.tell("Kill what?")

    def kill_myself(self, *args, **kwargs):
        player = kwargs['player']
        if self.wielded:
            player.tell("Wow you are wielding a weapon... FAileD TO CoMPUtE~")
        else:
            player.tell("You try to strangle yourself but that doesn't really work.")

    @verb('h*elp', ('any', 'any', 'any'))
    def help(self, *args, **kwargs):
        player = kwargs['player']
        player.tell("Unfortunately there is nobody here to help you right now.")

class Room(Root):
    def __init__(self):
        super().__init__()
        self.coords = None
        self.area_icon = Fore.WHITE + '. ' + Style.RESET_ALL
        self.map_icon = Fore.WHITE + Style.BRIGHT + '[]' + Style.RESET_ALL
        self.exits = []

    def render_map(self):
        # Location should be Area
        return self.location.render_map(self.coords, render_player=True)

    def render_description(self):
        return self.description

    def render_name(self):
        return Style.BRIGHT + self.name + Style.RESET_ALL

    def render_exits(self):
        s = Fore.CYAN + '[ exits: '
        for e in self.exits:
            s += Style.BRIGHT + e.name + ' '
        s += Style.NORMAL + ']'
        return s

    def render(self, *args, **kwargs):
        player = kwargs['player']
        lines = []
        i0 = 0
        m = self.render_map()
        if len(self.name) > 0:
            lines.append(m[0] + '  ' + self.render_name())
            i0 = 1
        rest = self.render_description()
        max_len = player.wrap - (6 * 2)
        for i in range(i0, len(m)):
            l = m[i]
            if len(rest) > 0:
                s, rest = string_utils.wrap(rest, max_len)
                lines.append(l + '  ' + s)
            else:
                lines.append(l)
        if len(rest) > 0:
            s, rest = string_utils.wrap(rest, max_len)
            lines.append(6 * '  ' + s)
        max_len = player.wrap
        while len(rest) > 0:
            s, rest = string_utils.wrap(rest, max_len)
            lines.append(s)
        return lines

class Area(Root):
    def __init__(self):
        super().__init__()
        self.levels = {}

    def render_map(self, origin, size=5, render_player=False):
        xo, yo, zo = origin
        m = [[] for y in range(5)]
        level_rooms, level_map = self.levels[zo]
        roomo = level_map[yo][xo]
        for row in range(5):
            for col in range(5):
                y = yo + row - 2
                x = xo + col - 2
                m[row].append(roomo.area_icon)
                if x >= 0 and y >= 0 and level_map[y][x]:
                    icon = level_map[y][x].map_icon
                    if x == xo and y == yo and render_player:
                        icon = Style.BRIGHT + Back.BLUE + Fore.WHITE + '()' + Style.RESET_ALL                    
                    m[row][col] = icon
        return [''.join(xs) for xs in m]

    def update(self):
        self.levels = {}
        mapped_room = lambda x: hasattr(x, 'coords') and x.coords
        rooms = [x for x in self.contents if mapped_room]
        for r in rooms:
            x, y, z = r.coords
            if not z in self.levels:
                level_map = [[None for y in range(64)] for x in range(64)]
                self.levels[z] = ([], level_map)
            level_rooms, level_map = self.levels[z]
            level_map[y][x] = r
            level_rooms.append(r)

def parse(player, s):
    tokens = tokenizer.tokenize(s)
    cmd = command.parse(tokens)
    return world.resolve(player, cmd)

def execute(cmd, player):
    if callable(cmd['f']):
        args = cmd['args']
        cmd.update({'player': player}) 
        cmd['f'](*args, **cmd)
    else:
        player.tell("That's not something you can do right now.")    

def prompt():
    return Style.BRIGHT + Fore.CYAN + "> " + Style.RESET_ALL

def loop():
    while True:
        s = input(prompt())
        if not s:
            continue
        cmd = parse(player, s)
        if player.debug:
            print(cmd)
        if cmd['verb'] == '@quit': 
            break
        execute(cmd, player)        

foo = Root()
foo.name = 'foo'

player = Player()
player.is_player = True
player.wielded = 'fubar'

DESTROYED_BUILDING = 'The foundation and a few walls remain but otherwise this building is completely destroyed.'
DAMP_CELLAR = 'The cellar is dark, damp and downright unpleasant.'

area = Area()

room = Room()
room.coords = (10, 10, 0)
room.name = 'Destroyed Building'
room.description = DESTROYED_BUILDING
world.move(room, area)
r1 = room

room = Room()
room.coords = (11, 10, 0)
room.name = "Vanity's Shack"
room.description = 'A small wooden shack seems a bit out of place.'
room.map_icon = Back.BLUE + Fore.YELLOW + Style.BRIGHT + 'Va' + Style.RESET_ALL
world.move(room, area)
r2 = room

exit = Exit()
exit.other_side = r2
exit.name = 'east'
r1.exits.append(exit)
exit.moveto(r1)

exit = Exit()
exit.other_side = r1
exit.name = 'west'
r2.exits.append(exit)
exit.moveto(r2)

room = Room()
room.coords = (11, 11, 0)
room.name = 'Destroyed Building'
room.description = DESTROYED_BUILDING
world.move(room, area)
r3 = room

exit = Exit()
exit.other_side = r3
exit.name = 'south'
r2.exits.append(exit)
exit.moveto(r2)

exit = Exit()
exit.other_side = r2
exit.name = 'north'
r3.exits.append(exit)
exit.moveto(r3)

room = Room()
room.coords = (9, 9, 0)
room.name = 'Destroyed Building'
room.description = DESTROYED_BUILDING
room.map_icon = Fore.YELLOW + '##' + Style.RESET_ALL
world.move(room, area)

room = Room()
room.coords = (10, 9, 0)
room.name = 'Destroyed Building'
room.description = DESTROYED_BUILDING
room.map_icon = Fore.YELLOW + '==' + Style.RESET_ALL
world.move(room, area)

room = Room()
room.coords = (11, 9, 0)
room.name = 'Destroyed Building'
room.description = DESTROYED_BUILDING
room.map_icon = Fore.YELLOW + '==' + Style.RESET_ALL
world.move(room, area)

room = Room()
room.coords = (12, 9, 0)
room.map_icon = Fore.YELLOW + '==' + Style.RESET_ALL
world.move(room, area)

room = Room()
room.coords = (9, 10, 0)
room.map_icon = Fore.YELLOW + '||' + Style.RESET_ALL
world.move(room, area)

room = Room()
room.coords = (9, 11, 0)
room.map_icon = Fore.YELLOW + '||' + Style.RESET_ALL
world.move(room, area)

room = Room()
room.coords = (9, 12, 0)
room.map_icon = Fore.YELLOW + '||' + Style.RESET_ALL
world.move(room, area)

room = Room()
room.coords = (0, 12, -1)
room.name = 'Damp Cellar'
room.description = DAMP_CELLAR
room.map_icon = '[]'
world.move(room, area)
world.move(player, room)
world.move(foo, room)
r4 = room

exit = Exit()
exit.name = 'up'
exit.other_side = r3
r4.exits.append(exit)
exit.moveto(r4)

exit = Exit()
exit.name = 'down'
exit.other_side = r4
r3.exits.append(exit)
exit.moveto(r3)

room = Room()
room.coords = (1, 12, -1)
room.name = 'Damp Cellar'
room.description = DAMP_CELLAR
room.map_icon = Style.BRIGHT + Fore.WHITE + Back.MAGENTA + "BR" + Style.RESET_ALL
world.move(room, area)
r5 = room

exit = Exit()
exit.name = 'east'
exit.other_side = r5
r4.exits.append(exit)
exit.moveto(r4)

exit = Exit()
exit.name = 'west'
exit.other_side = r4
r5.exits.append(exit)
exit.moveto(r5)

room = Room()
room.coords = (1, 12, -2)
room.name = 'The Pit'
room.map_icon = 'XX'
room.area_icon = '//'
world.move(room, area)
r6 = room

exit = Exit()
exit.name = 'down'
exit.other_side = r6
r5.exits.append(exit)
exit.moveto(r5)

exit = Exit()
exit.name = 'up'
exit.other_side = r5
r6.exits.append(exit)
exit.moveto(r6)

area.update()

if __name__ == '__main__':
    loop()