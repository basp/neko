import libtcodpy as libtcod
import random

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class Cell:
    def __init__(self):
        self.walls = set([NORTH, EAST, SOUTH, WEST])

    def remove_wall(self, direction):
        self.walls -= {direction}

    def has_wall(self, direction):
        return direction in self.walls

WIDTH = 32
HEIGHT = 32

XOFFSET = (-1, 0, 1, 0)
YOFFSET = (0, 1, 0, 1)

opposite = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    WEST: EAST,
    EAST: WEST
}

def unvisited_neighbors(x, y, nr, nc, unvisited):
    r = []
    for i in range(len(XOFFSET)):
        nx, ny = x + XOFFSET[i], y + YOFFSET[i]
        if nx < 0 or nx >= nc:
            continue
        if ny < 0 or ny >= nr:
            continue
        if (nx, ny) in unvisited:
            r.append((nx, ny))
    return r


m = [[Cell() for y in range(HEIGHT)] for x in range(WIDTH)]
unvisited = set([(x, y) for y in range(HEIGHT) for x in range(WIDTH)])

current = (0, 1)
unvisited -= {current}

stack = []

while unvisited:
    cx, cy = current
    neighbors = unvisited_neighbors(cx, cy, HEIGHT, WIDTH, unvisited)
    if neighbors:
        i = random.randint(0, len(neighbors) - 1)
        stack.append(current)
        nx, ny = neighbors[i]
        m[x][y].remove_wall(i)
        m[nx][ny].remove_wall(opposite[i])
        current = (nx, ny)
        unvisited -= {current}
    elif stack:
        cx, cy = stack.pop()
    else:
        current = unvisited.pop()

s = []
for y in range(HEIGHT):
    l1 = ''
    l2 = ''
    for x in range(WIDTH):
        if m[x][y].has_wall(EAST):
            l1 += '01'
        else:
            l1 += '00'
        
        if m[x][y].has_wall(SOUTH):
            l2 += '11'
        else:
            l2 += '01'
    s.append(l1)
    s.append(l2)

libtcod.console_init_root(len(s[0]), len(s), 'Test', False)
while not libtcod.console_is_window_closed():
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_clear(0)

    for y in range(len(s)):
        for x in range(len(s[y])):
            if s[y][x] == '0':
                color = libtcod.white
            else:
                color = libtcod.black
            libtcod.console_set_char_background(0, x, y, color, libtcod.BKGND_SET)

    libtcod.console_flush()
    libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)