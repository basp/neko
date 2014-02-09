import match
import verb

class Object:
    def __init__(self, name=''):
        self.name = name
        self.location = None
        self.contents = set()
        self.is_player = False

    def names(self):
        return {self.name}

    def title(self):
        return self.name

    def move(self, where):
        if self.location:
            self.location.contents -= {self}
        self.location = where
        where.contents |= {self}
        return self

def _resolve_objstr(player, objstr, objs):
    if objstr == "me":
        return player
    elif objstr == "here":
        return player.location
    else:
        return match.object(objstr, player.contents)
  
def _resolve_verb(verbstr, objs):
    for o in objs:
        verbs = verb.verbs(o)
        for v in verbs:
            names, args = v.__dict__['names'], v.__dict__['args']
            names = names.split(' ')
            for n in names:
                if match.verb(verbstr, n):
                    return v

def resolve(player, cmd):
    dobjstr, iobjstr = cmd['dobjstr'], cmd['iobjstr']

    dobj = _resolve_objstr(player, dobjstr, player.contents)
    if dobj is None and player.location:
        dobj = match.object(dobjstr, player.location.contents)

    iobj = _resolve_objstr(player, iobjstr, player.contents)
    if iobj is None and player.location:
        iobj = match.object(iobjstr, player.location.contents)

    cmd['dobj'] = dobj
    cmd['iobj'] = iobj

    verbstr = cmd['verb']
    objs = [player, player.location, dobj, iobj]
    cmd['f'] = _resolve_verb(verbstr, objs)

    return cmd