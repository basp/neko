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

import command
import match
import random
import string_utils
import tokenizer
import world

from verb import verb
from ansi import Style, Fore, Back

DEFAULT_DEBUG = False
MIN_WRAP = 40
DEFAULT_WRAP = 80

class Root(world.Object):
    def __init__(self):
        super().__init__()
        self.description = 'Nothing out of the ordinary.'

    def title(self):
        return self.name

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
        self.dur = 10

    def invoke(self, what, *args, **kwargs):
        if self.other_side:
            what.moveto(self.other_side)
        return self.dur

    def look_self(self, *args, **kwargs):
        if self.other_side:
            d = self.other_side.render(*args, **kwargs)
            mobs = self.other_side.render_mobs(*args, **kwargs)
            if mobs:
                d.append('')
                d += mobs
            return d

class Thing(Root):
    def __init__(self):
        super().__init__()

    def title(self):
        s = self.name
        if s.startswith(('a', 'e', 'i', 'u', 'o', 'A', 'E', 'I', 'U', 'O')):
            return 'an ' + self.name
        else:
            return 'a ' + self.name

class Player(Root):
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
            mobs = self.location.render_mobs(*args, **kwargs)
            if mobs:
                d.append('')
                d += mobs
            things = self.location.render_things(*args, **kwargs)
            if things:
                d.append('')
                d += things
            exits = self.location.render_exits(*args, **kwargs)
            if exits:
                d.append('')
                d += exits
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
        return self.go(self, *args, **kwargs)

    @verb('g*o', ('any', 'none', 'none'))
    def go(self, *args, **kwargs):
        dobjstr = kwargs['dobjstr']
        exit = match.object(dobjstr, self.location.exits)
        if exit is match.Ambiguous:
            player.tell("I'm not sure which way `%s' you mean." % dobjstr)
        elif exit:
            dur = exit.invoke(self, *args, **kwargs)
            player.look_around(*args, **kwargs)
            return dur
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

    def kill_self(self, *args, **kwargs):
        player = kwargs['player']
        if self.wielded:
            player.tell("You are not THAT desperate!")
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
        # Location should be an Area instance
        return self.location.render_map(self.coords, render_player=True)

    def render_description(self, *args, **kwargs):
        return self.description

    def render_name(self, *args, **kwargs):
        return Style.BRIGHT + self.name + Style.RESET_ALL

    def render_exits(self, *args, **kwargs):
        player = kwargs['player']
        if not self.exits:
            return []
        s = Fore.CYAN + '[ exits: '
        for e in self.exits:
            s += Style.BRIGHT + e.name + ' '
        s += Style.NORMAL + ']'
        return string_utils.wrap_to_lines(s, player.wrap)

    def render(self, *args, **kwargs):
        player = kwargs['player']
        lines = []
        i0 = 0
        m = self.render_map()
        if len(self.name) > 0:
            lines.append(m[0] + '  ' + self.render_name(*args, **kwargs))
            i0 = 1
        # TODO: Fix this so we can pass in map size
        rest = self.render_description(*args, **kwargs)
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

    def render_things(self, *args, **kwargs):
        player = kwargs['player']
        things = [x.title() for x in self.contents if isinstance(x, Thing)]
        if not things:
            return []
        d = "You see %s on the floor." % string_utils.english_list(things)
        return string_utils.wrap_to_lines(d, player.wrap)

    def render_mobs(self, *args, **kwargs):
        player = kwargs['player']
        mobs = [x for x in self.contents if isinstance(x, Mob)]
        if not mobs:
            return []
        d = ""
        groups = {}
        for m in mobs:
            doing = m.doing()
            if not doing in groups:
                groups[doing] = []
            groups[doing].append(m.title())
        for doing in groups:
            actors = groups[doing]
            verb = "is"
            if len(actors) > 1:
                verb = "are"
            d += "%s %s %s here." % (string_utils.english_list(actors), verb, doing)
        return string_utils.wrap_to_lines(d, player.wrap)

class Area(Root):
    def __init__(self):
        super().__init__()
        self.levels = {}

    def render_map(self, origin, render_player=False):
        xo, yo, zo = origin
        m = [[] for y in range(5)]
        level_rooms, level_map = self.levels[zo]
        roomo = level_map[yo][xo]
        for row in range(5):
            for col in range(5):
                y = yo + row - (5 // 2)
                x = xo + col - (5 // 2)
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


class Actor(Root):
    def __init__(self):
        super().__init__()

    def act(self, time):
        pass

class Mob(Actor):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.doing_msg = 'standing'

    def doing(self):
        return self.doing_msg

    def title(self):
        return self.name

class Alana(Mob):
    def __init__(self):
        super().__init__('Alana')
        self.description = 'A big (for a cat at least) orange furball. He looks up at you curiously.'
        self.doing_msg = 'walking around'

    def act(self, time, *args, **kwargs):
        player = kwargs['player']
        if not self.location and self.location.exits:
            return
        if random.randint(0, 10) < 3:
            i = random.randint(0, len(self.location.exits) - 1)
            exit = self.location.exits[i]
            return exit.invoke(self) # TODO: incorporate duration

class World:
    def __init__(self):
        self.mobs = []

def parse(player, s):
    tokens = tokenizer.tokenize(s)
    cmd = command.parse(tokens)
    return world.resolve(player, cmd)

def execute(cmd, player, actors=[]):
    if callable(cmd['f']):
        args = cmd['args']
        cmd.update({'player': player}) 
        dur = cmd['f'](*args, **cmd)
        if dur and dur > 0:
            for actor in actors:
                actor.act(time=dur, *args, **cmd)
    else:
        player.tell("That's not something you can do right now.")    

def prompt():
    return Style.BRIGHT + Fore.CYAN + "> " + Style.RESET_ALL

def loop(actors=[]):
    while True:
        s = input(prompt())
        if not s:
            continue
        cmd = parse(player, s)
        if player.debug:
            print(cmd)
        if cmd['verb'] == '@quit': 
            break
        r = execute(cmd, player, actors)

foo = Thing()
foo.name = 'rusty nail'
foo.aliases = {'nail'}
foo.description = "A rusty casing nail. It's a little crooked."

bar = Thing()
bar.name = 'orange'
bar.description = "It's covered in mold. It's probably a bad idea to eat this."

alana = Alana()

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
world.move(alana, room)
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
room.map_icon = Fore.YELLOW + '##' + Style.RESET_ALL
world.move(room, area)

room = Room()
room.coords = (10, 9, 0)
room.map_icon = Fore.YELLOW + '==' + Style.RESET_ALL
world.move(room, area)

room = Room()
room.coords = (11, 9, 0)
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
world.move(bar, room)
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
    loop([alana])