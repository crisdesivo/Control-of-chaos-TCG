import pyxel
import random
from scr.card import *
from ui.card_display import CardDisplay
from ui.hand_gui import HandGUI, CARD_DRAW_HEiGHT, CARD_DRAW_WIDTH
from ui.constants import ENERGY_COLORS, ENERGY_SPRITES
from ui.components import Components


class UserInterface:
    def __init__(self):
        pyxel.init(256, 256)
        pyxel.mouse(True)
        pyxel.load("assets/my_resource.pyxres")

        self.components = Components()

    def initComponents(self, match, firstplayer):
        self.match = match
        self.initHandGUI(firstplayer)

        # Components that must be on top
        self.cardDisplay = CardDisplay()
        self.components.add(self.cardDisplay, draw=False, update=False)

    def initHandGUI(self, firstplayer):
        self.handGUI = HandGUI(self.match.players[firstplayer].hand)
        self.handGUI.drawCard = self.drawCard
        self.handGUI.checkCard = self.checkHandCard
        self.components.add(self.handGUI)

    def update(self):
        self.components.update()

    def draw(self):
        pyxel.cls(4)
        self.components.draw()
        pyxel.flip()

    def drawCard(self, card, x, y):
        if card.cardType == 0:
            self.drawEnergyCard(card, x, y)
        if card.cardType == 1:
            self.drawUnitCard(card, x, y)

    def drawUnitCard(self, card, x, y):
        pyxel.rect(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEiGHT, 6)
        pyxel.rectb(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEiGHT, 0)
        text = "\n".join(card.name.split())
        pyxel.text(x + 2, y + 2, text, 0)
        self.drawHP(card.hp, card.maxHP, x, y)

    def drawHP(self, hp, maxHP, x, y):
        sep = 5
        r = 3
        startX = x + 4
        startY = y + CARD_DRAW_WIDTH - 5
        for i in range(maxHP):
            if i < hp:
                pyxel.circ(startX, startY, r, col=0)
            else:
                pyxel.circ(startX, startY, r, col=7)
                pyxel.circb(startX, startY, r, col=0)

    def drawEnergyCard(self, card, x, y):
        pyxel.rect(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEiGHT,
                   ENERGY_COLORS[card.energyType])
        pyxel.rectb(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEiGHT, 0)
        text = "\n".join(card.name.split())
        pyxel.text(x + 2, y + 2, text, 0)
        pyxel.blt(
            x + 12,
            y + 25, 0,
            *ENERGY_SPRITES[card.energyType],
            colkey=4)

    def selectTarget(self, possibleTargets):
        pass

    def selectSlot(self, possibleSlots):
        pass

    def selectTechnique(self, unit):
        pass

    def selectPlay(self, player):
        while True:
            self.update()
            self.draw()

    def swapPlayers(self):
        pass

    def checkHandCard(self, card):
        self.cardDisplay.card = card
        self.cardDisplay.playable = card.playable(self.match)
        self.cardDisplay.usable = False
        self.components.resume(self.cardDisplay)
        self.components.freeze(self.handGUI)

    def checkEnemyUnitCard(self, card):
        pass

    def checkUnitCard(self, card):
        pass


if __name__ == "__main__":
    gui = UserInterface()
