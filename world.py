class Object:
    def __init__(self):
        self.name = ''
        self.location = None
        self.contents = {}
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