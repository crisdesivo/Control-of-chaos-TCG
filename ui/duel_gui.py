import pyxel
import random
import time
from scr.card import *
from ui.card_display import CardDisplay
from ui.hand_gui import HandGUI, CARD_DRAW_HEIGHT, CARD_DRAW_WIDTH
from ui.constants import ENERGY_COLORS, ENERGY_SPRITES
from ui.components import Components


class DuelGUI:
    def __init__(self):
        pyxel.init(256, 256)
        pyxel.mouse(True)
        pyxel.load("assets/my_resource.pyxres")

        self.components = Components()

    def initComponents(self, duel, firstplayer):
        self.duel = duel
        self.initHandGUI(firstplayer)

        # Components that must be on top
        self.cardDisplay = CardDisplay(self)
        self.components.add(self.cardDisplay, draw=False, update=False)

    def initHandGUI(self, firstplayer):
        self.handGUI = HandGUI(self.duel.players[firstplayer].hand)
        self.handGUI.checkCard = self.checkHandCard
        self.components.add(self.handGUI)

    def update(self):
        self.components.update()

    def draw(self):
        pyxel.cls(4)
        self.components.draw()
        pyxel.flip()

    def remove(self, component):
        self.components.remove(component)

    def selectTarget(self, possibleTargets):
        pass

    def selectSlot(self, possibleSlots):
        pass

    def selectTechnique(self, unit):
        pass

    def selectPlay(self, player):
        while True:
            startFrameTime = time.time()
            self.update()
            self.draw()
            time.sleep(1./60. - min(1./60., time.time() - startFrameTime))

    def swapPlayers(self):
        pass

    def checkHandCard(self, card):
        self.components.freeze(self.handGUI)
        self.cardDisplay.open(card,
                              card.playable(self.duel),
                              usable=False)
        self.components.resume(self.cardDisplay)

    def checkEnemyUnitCard(self, card):
        pass

    def checkUnitCard(self, card):
        pass
