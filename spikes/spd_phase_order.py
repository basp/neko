class Entity:
    def __init__(self, name, spd):
        self.name = name
        self.spd = spd

phases = ['fast', 'normal', 'slow', 'quick', 'normal']
phase_dict = {
    'fast'      : ('fast', 'normal', 'slow'),
    'normal'    : ('normal', 'slow'),
    'slow'      : ('slow'),
    'quick'     : ('normal', 'slow', 'quick'),
    'fast'      : ('normal', 'slow', 'quick', 'fast')
}

phase = phases[0]
phase_count = 0

entities = [
    Entity('foo', 'fast'),
    Entity('bar', 'slow'),
    Entity('quux', 'normal')
]

while True:
    phase_count = phase_count % len(phases)
    phase = phases[phase_count]
    print('[ ' + phase + ' ]')
    for x in entities:
        if phase in phase_dict[x.spd]:
            print(x.name, "acts")
    cmd = input('> ')
    phase_count += 1