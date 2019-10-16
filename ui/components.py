class Components:
    def __init__(self):
        self.drawSet = set()
        self.updateSet = set()
        self.all = set()

    def add(self, component, draw=True, update=True):
        self.all.add(component)
        if draw:
            self.drawSet.add(component)
        if update:
            self.updateSet.add(component)

    def update(self):
        for component in self.updateSet:
            component.update()

    def draw(self):
        for component in self.drawSet:
            component.draw()

    def freeze(self, component):
        self.updateSet.remove(component)

    def hide(self, component):
        self.drawSet.remove(component)

    def pause(self, component):
        self.freeze(component)
        self.hide(component)

    def unfreeze(self, component):
        if component in self.all:
            self.updateSet.add(component)

    def unhide(self, component):
        if component in self.all:
            self.drawSet.add(component)

    def resume(self, component):
        self.unfreeze(component)
        self.unhide(component)