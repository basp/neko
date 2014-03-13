class Mob:
    def __init__(self, name, spd):
        self.spd = spd
        self.dt = self.spd
        pass

    def act(self, dur, *args, **kwargs):
        self.dt -= dur
        if self.dt <= 0:
            print(self.name, 'acts')
            self.dt = self.spd   

class Player:
    def __init__(self):
        pass

    def act(self, *args, **kwargs):
        return 10

player = Player()
ene1 = Mob(10)
ene2 = Mob(20)
mobs = [ene1, ene2]
while True:
    inp = input('> ')
    dur = player.act()
    for m in mobs: