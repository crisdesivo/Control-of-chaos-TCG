class Turn:
    def __init__(self, player=None, match=None):
        self.player = player
        self.energyPlayed = None
        self.unitPlayed = None
        self.techniquesPlayed = []
        self.match = match
        self.endTurn = False

    def selectTarget(self, possibleTargets):
        return self.match.selectTarget(possibleTargets)

    def addAttack(self, technique, attacker):
        possibleTargets = self.match.oponentUnits()
        target = self.match.selectTarget(possibleTargets)
        target.receiveAttack(attacker, technique)
        for effect in technique.effects:
            effect.activate(self)
        self.endTurn = True

    def run(self):
        if self.match.turnNumber < 2:
            for _ in range(3):
                self.match.players[self.player].drawCard()
        else:
            self.match.players[self.player].drawCard()
        while not self.endTurn:
            endTurn = self.match.selectPlay(self.player)
            if endTurn:
                self.endTurn = True
