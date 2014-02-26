class Room:
    def __init__(self, coords, map_icon, area_icon):
        self.coords = coords
        self.map_icon = map_icon
        self.area_icon = area_icon
        self.map = []

r1 = Room((0, 0, 0), 'R1', '//')
r2 = Room((1, 0, 0), 'R2', '//')
r3 = Room((0, 1, 0), 'R3', '//')
r4 = Room((3, 0, 0), 'R4', '//')
r5 = Room((3, 1, 0), 'R5', '//')
r6 = Room((2, 1, 0), 'R6', '//')

area = [r1, r2, r3, r4, r5, r6]

bigmap = [[None for y in range(64)] for x in range(64)]
for r in area:
    x, y, z = r.coords
    bigmap[y][x] = r

for r in area:
    rx, ry, rz = r.coords
    m = [[] for y in range(5)]
    for i in range(5):
        for j in range(5):
            y = ry + i - 2
            x = rx + j - 2
            m[i].append(r.area_icon)
            if x >= 0 and y >= 0 and bigmap[y][x]:
                m[i][j] = bigmap[y][x].map_icon
    r.map = [''.join(xs) for xs in m]

def print_map(r):
    for l in r.map:
        print(l)

for r in area:
    print_map(r)
    print()
