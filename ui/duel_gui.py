import pyxel
import random
import time
from scr.card import *
from ui.card_display import CardDisplay
from ui.hand_gui import HandGUI, CARD_DRAW_HEIGHT, CARD_DRAW_WIDTH
from ui.constants import ENERGY_COLORS, ENERGY_SPRITES
from ui.board_gui import BoardGUI


class DuelGUI:
    def __init__(self):
        pyxel.init(256, 256)
        pyxel.mouse(True)
        pyxel.load("assets/my_resource.pyxres")

        # self.components = Components()
        self.duel = None

        self.brackgroundComponents = []
        self.foreGroundComponents = []
        self.overlayComponents = []
        self.handGUI = None
        self.boardGUI = None
        self.cardDisplay = None

    def addToBackground(self, component):
        self.brackgroundComponents.append(component)

    def addToForeground(self, component):
        self.foreGroundComponents.append(component)

    def addToOverlays(self, component):
        self.overlayComponents.append(component)

    def initComponents(self, duel, firstplayer):
        self.duel = duel
        self.initHandGUI(firstplayer)
        self.boardGUI = BoardGUI(self)
        self.addToForeground(self.boardGUI)

        self.cardDisplay = CardDisplay(self)
        self.addToOverlays(self.cardDisplay)

    def initHandGUI(self, firstplayer):
        self.handGUI = HandGUI(self.duel.players[firstplayer].hand)
        self.handGUI.checkCard = self.checkHandCard
        self.addToForeground(self.handGUI)

    def update(self):
        self.cardDisplay.update()
        self.handGUI.update()
        self.boardGUI.update()

    def draw(self):
        pyxel.cls(4)
        self.drawForeground()
        self.drawOverlays()
        pyxel.flip()

    def drawForeground(self):
        for component in self.foreGroundComponents:
            component.draw()

    def drawOverlays(self):
        for component in self.overlayComponents:
            component.draw()

    def drawBackground(self):
        for component in self.brackgroundComponents:
            component.draw()

    def freezeForeground(self):
        for component in self.foreGroundComponents:
            component.freeze = True

    def unfreezeForeground(self):
        for component in self.foreGroundComponents:
            component.unfreeze = True

    def selectTarget(self, possibleTargets):
        return self.boardGUI.selectTarget(possibleTargets)

    def selectSlot(self, possibleSlots):
        print("gui select")
        target = self.boardGUI.selectTarget(possibleSlots)
        return target

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
        self.freezeForeground()
        self.cardDisplay.open(card,
                              card.playable(self.duel),
                              usable=False)

    def checkBoardCard(self, card):
        self.freezeForeground()
        self.cardDisplay.open(card,
                              card.playable(self.duel),
                              usable=False)

    def checkEnemyUnitCard(self, card):
        pass

    def checkUnitCard(self, card):
        pass
