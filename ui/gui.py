import pyxel
from scr.card import *
import random

ENERGY_COLORS = [
    8,
    12,
    3,
    7,
    5
]

ENERGY_SPRITES = [
    (32, 0, 16, 16),
    (16, 0, 16, 16),
    (0, 16, 16, 16),
    (16, 16, 16, 16),
    (0, 0, 16, 16)
]


class UserInterface:
    match = None

    def __init__(self, handGUI):
        pyxel.init(256, 256)
        pyxel.mouse(True)
        pyxel.load("assets/my_resource.pyxres")

        self.handGUI = handGUI
        self.handGUI.drawCard = self.drawCard
        pyxel.run(self.update, self.draw)

        # self.draw()
        # pyxel.flip()

    def update(self):
        self.handGUI.update()
        pass

    def draw(self):
        pyxel.cls(4)
        self.handGUI.draw()

    def drawCard(self, card, x, y):
        if card.cardType == 0:
            self.drawEnergyCard(card, x, y)

    def drawEnergyCard(self, card, x, y):
        pyxel.rect(x, y, 40, 60, ENERGY_COLORS[card.energyType])
        pyxel.rectb(x, y, 40, 60, 0)
        text = "\n".join(card.name.split())
        pyxel.text(x + 2, y + 2, text, 0)
        pyxel.blt(x + 12, y + 25, 0, *ENERGY_SPRITES[card.energyType], colkey=4)

    def startGameMatch(self, match):
        self.match = match

    def selectTarget(self, possibleTargets):
        pass

    def selectSlot(self, possibleSlots):
        pass

    def selectTechnique(self, unit):
        pass

    def selectPlay(self, player):
        pass

    def swapPlayers(self):
        pass

    def checkHandCard(self, card):
        pass

    def checkEnemyUnitCard(self, card):
        pass

    def checkUnitCard(self, card):
        pass


if __name__ == "__main__":
    gui = UserInterface()
