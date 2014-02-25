phases = ['fast', 'normal', 'slow', 'quick', 'normal']
phase_dict = {
    'fast'      : ('fast', 'normal', 'slow'),
    'normal'    : ('normal', 'slow'),
    'slow'      : ('normal'),
    'quick'     : ('normal', 'slow', 'quick'),
    'fast'      : ('normal', 'slow', 'quick', 'fast')
}

phase = phases[0]
phase_count = 0

while True:
    phase_count = phase_count % len(phases)
    phase = phases[phase_count]
    print('[ ' + phase + ' ]')
    cmd = input('> ')
    phase_count += 1