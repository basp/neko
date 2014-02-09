# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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
  
def _resolve_verb(cmd, objs):
    verbstr = cmd['verb']
    for o in objs:
        verbs = verb.verbs(o)
        for v in verbs:
            names, args = v.__dict__['names'], v.__dict__['args']
            if match.verbargs(o, args, cmd):
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

    objs = [player, player.location, dobj, iobj]
    cmd['f'] = _resolve_verb(cmd, objs)

    return cmd