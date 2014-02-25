class Entity:
    def __init__(self, name, spd, next=lambda: None):
        self.name = name
        self.spd = spd
        self.next = next

    def act(self):
        if callable(self.next):
            self.next = self.next()

phases = ['fast', 'normal', 'slow', 'quick', 'normal']
phase_dict = {
    'slow'      : ('slow'),
    'normal'    : ('normal', 'slow'),
    'quick'     : ('normal', 'slow', 'quick'),
    'fast'      : ('normal', 'slow', 'quick', 'fast')
}

phase = phases[0]
phase_count = 0

def test(name):
    print(name, 'looks around.')
    return lambda: test(name)

entities = [
    Entity('foo', 'slow', next=lambda: test('foo')),
    Entity('bar', 'normal'),
    Entity('quux', 'fast')
]

while True:
    phase_count = phase_count % len(phases)
    phase = phases[phase_count]
    print('[ ' + phase + ' ]')
    for x in entities: 
        if phase in phase_dict[x.spd]: 
            x.act()
    cmd = input('> ')
    phase_count += 1