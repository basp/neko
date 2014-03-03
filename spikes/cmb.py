class Mobile:
    def __init__(self, name, t):
        self.name = name
        self.t = t  # time in between acting
        self.tr = t # time to rest before next action

    def act(self, delta):
        self.tr -= delta
        if self.tr <= 0:
            print(self.name)
            self.tr = self.t + self.tr

START_TIME = (10, 20, 20)

mobs = [
    Mobile('foo', 10),
    Mobile('bar', 15)
]

def atk(s):
    if s == 'pow':
        return 10
    else:
        return 5

turn = 0
if __name__ == '__main__':
    while True:
        turn += 1
        try:
            s = input(str(turn) + '> ')
            t = atk(s)
            print('p (%s)' % s)        
            for m in mobs: 
                m.act(t)
            # TODO: Handle input
        except EOFError:
            break
