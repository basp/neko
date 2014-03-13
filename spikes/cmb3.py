class Mob:
    def __init__(self, name, q):
        self.name = name
        self.q = q  # lower is better (0 is lightspeed, invalid for mobs)
        self.t = 0
        
    def act(self, dur):
        self.t += dur
        c = self.t // self.q
        self.t = self.t % self.q
        return (c, self.t)

foo = Mob('foo', 10)
bar = Mob('bar', 20)

if __name__ == '__main__':
    x = 3
    print(foo.act(x))
    print(foo.act(x))
    print(foo.act(x))
    print(foo.act(x))
    print(foo.act(x))
    print(foo.act(x))
    print(foo.act(x))
    print(foo.act(x))