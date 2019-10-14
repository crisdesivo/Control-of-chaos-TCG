class Board:
    def __init__(self, deck1, deck2):
        self.fullDecks = [deck1, deck2]
        self.units = [[None, None, None, None, None],
                      [None, None, None, None, None]]
        self.energies = [[], []]
        self.graveyards = [[], []]
        self.decks = [deck1, deck2]
        self.boardUI = BoardUI()


class BoardUI:
    pass