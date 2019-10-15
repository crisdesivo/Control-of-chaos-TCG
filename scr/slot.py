class Slot:
    occupant = None
    isPlayable = True

    def __init__(self, location=None, player=None):
        self.location = location
        self.player = player
        self.name = "Empty Slot"
