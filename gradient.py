import libtcodpy as libtcod
import utils

def gray_scale():
    g = Gradient()
    g.add_point(-1.0, libtcod.Color(0, 0, 0))
    g.add_point(1.0, libtcod.Color(255, 255, 255))
    return g

def terrain():
    g = Gradient()
    g.add_point(-1.00, libtcod.Color(0, 0, 64))
    g.add_point(-0.40, libtcod.Color(32, 64, 128))
    g.add_point(-0.20, libtcod.Color(64, 96, 192))
    g.add_point(-0.02, libtcod.Color(192, 192, 128))
    g.add_point(0.00, libtcod.Color(0, 192, 0))
    g.add_point(0.40, libtcod.Color(0, 128, 0))
    g.add_point(0.60, libtcod.Color(32, 128, 32))
    g.add_point(0.65, libtcod.Color(128, 96, 64))
    g.add_point(0.75, libtcod.Color(128, 96, 96))
    g.add_point(0.85, libtcod.Color(128, 255, 255))
    g.add_point(1.00, libtcod.Color(255, 255, 255))
    return g

class Point:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

class Gradient:
    def __init__(self):
        self.points = []

    def _find_index_pos(self, pos):
        for i in range(len(self.points)):
            if pos < self.points[i].pos:
                return i
        return len(self.points)

    def add_point(self, pos, color):
        insert_pos = self._find_index_pos(pos)
        self.points.insert(insert_pos, Point(pos, color))

    def get_color(self, pos):
        index_pos = self._find_index_pos(pos)

        i0 = utils.clamp(index_pos - 1, 0, len(self.points) - 1)
        i1 = utils.clamp(index_pos, 0, len(self.points) - 1)
        
        if i0 == i1:
            return self.points[i0].color

        inp0 = self.points[i0].pos
        inp1 = self.points[i1].pos
        
        a = (pos - inp0) / (inp1 - inp0)
        
        c0 = self.points[i0].color
        c1 = self.points[i1].color

        return libtcod.Color(
            int(utils.lerp(c0.r, c1.r, a)),
            int(utils.lerp(c0.g, c1.g, a)),
            int(utils.lerp(c0.b, c1.b, a)))