class Deck:
    def __init__(self):
        self.cards = []
    
    def drawCard(self):
        if len(self.cards) > 0:
            return self.cards.pop(-1)