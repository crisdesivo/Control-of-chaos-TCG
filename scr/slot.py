"""
Class Slot: Placeholder for cards or sets of cards
"""


class Slot:
    """Placeholder for cards or sets of cards
    """
    occupant = None
    isPlayable = True

    def __init__(self, parent, location=None, player=None):
        """Placeholder for cards or sets of cards

        Keyword arguments:
        parent -- Board where the slot is
        location -- Integer, index, location of the slot in the board
        player -- Integer, player that controls this slot
        """
        self.parent = parent
        self.location = location
        self.player = player
        self.name = "Empty Slot"

    def place(self, occupant):
        """Places an occupant on itself

        Keyword arguments:
        occupant -- Object that will occupy the slot
        """
        if self.occupant is None:
            self.occupant = occupant
            self.occupant.parent = self
            self.name = "Occupied Slot"
        else:
            self.occupant.attach(occupant)

    def empty(self):
        """Empties the slot"""
        self.occupant = None
        self.name = "Empty Slot"
