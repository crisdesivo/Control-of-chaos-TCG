"""
Class DuelGUI: Duel graphic user interface
"""
import pyxel
import random
import time
from scr.card import *
from ui.card_display import CardDisplay
from ui.hand_gui import HandGUI, CARD_DRAW_HEIGHT, CARD_DRAW_WIDTH
from ui.constants import ENERGY_COLORS, ENERGY_SPRITES
from ui.board_gui import BoardGUI


class DuelGUI:
    """
    Duel graphic user interface
    """
    def __init__(self):
        """
        Duel graphic user interface
        """
        pyxel.init(256, 256)
        pyxel.mouse(True)
        pyxel.load("assets/my_resource.pyxres")
        pyxel.image(2).load(0, 0, "assets/good_neighbors.png")

        # self.components = Components()
        self.duel = None

        self.handGUI = None
        self.boardGUI = None
        self.cardDisplay = None

    def addToBackground(self, component):
        """
        Adds the input component to the list of background components
        """
        self.brackgroundComponents.append(component)

    def addToForeground(self, component):
        """
        Adds the input component to the list of foreground components
        """
        self.foregroundComponents.append(component)

    def addToOverlays(self, component):
        """
        Adds the input component to the list of overlay components
        """
        self.overlayComponents.append(component)

    def initComponents(self, duel, firstplayer):
        """
        Initializes the components of the graphic interface

        Keyword arguments:
        duel -- Duel of the interface
        firstplayer -- Integer, index (0 or 1), of the player who goes first
        """
        self.brackgroundComponents = []
        self.foregroundComponents = []
        self.overlayComponents = []

        self.duel = duel
        self.initHandGUI(firstplayer)

        self.boardGUI = BoardGUI(self)
        self.addToForeground(self.boardGUI)

        self.cardDisplay = CardDisplay(self)
        self.addToOverlays(self.cardDisplay)

    def initHandGUI(self, firstplayer):
        """
        Initializes the hand graphic interface component

        Keyword arguments:
        firstplayer -- Integer, index (0 or 1), of the player who goes first
        """
        self.handGUI = HandGUI(self.duel.players[firstplayer].hand)
        self.handGUI.checkCard = self.checkHandCard
        self.addToForeground(self.handGUI)

    def update(self):
        """
        Updates the GUI
        """
        ret = self.cardDisplay.update()
        self.handGUI.update()
        self.boardGUI.update()
        return ret

    def draw(self):
        """
        Draws the GUI
        """
        self.drawBackground()
        self.drawForeground()
        self.drawOverlays()
        pyxel.flip()

    def drawBackground(self):
        """
        Draws the background components
        """
        pyxel.cls(4)
        for component in self.brackgroundComponents:
            component.draw()

    def drawForeground(self):
        """
        Draws the foreground components
        """
        for component in self.foregroundComponents:
            component.draw()

    def drawOverlays(self):
        """
        Draws the overlays components
        """
        for component in self.overlayComponents:
            component.draw()

    def freezeForeground(self):
        """
        Freezes the foreground components
        """
        for component in self.foregroundComponents:
            component.freeze = True

    def unfreezeForeground(self):
        """
        UnFreezes the foreground components
        """
        for component in self.foregroundComponents:
            component.unfreeze = True

    def selectTarget(self, possibleTargets):
        """Gives the player the ability to choose a target from a list
        and returns the choice.

        Keyword arguments:
        possibleTargets -- List of possible targets to choose from
        """
        return self.boardGUI.selectTarget(possibleTargets)

    def selectSlot(self, possibleSlots):
        """Gives the player the ability to choose a slot from a list of slots
        and returns the choice.

        Keyword arguments:
        possibleTargets -- List of possible targets to choose from
        """
        print("gui select")
        target = self.boardGUI.selectTarget(possibleSlots)
        return target

    def runTurn(self):
        """
        Runs a turn in the duel until the turn ends
        """
        self.endTurn = False
        while not self.endTurn:
            startFrameTime = time.time()
            self.update()
            self.draw()
            time.sleep(1./60. - min(1./60., time.time() - startFrameTime))

    def checkHandCard(self, card):
        """Show a card from the hand in more details

        Keyword arguments:
        card -- Card from the hand
        """
        self.freezeForeground()
        self.cardDisplay.open(card,
                              card.playable(self.duel),
                              usable=False)

    def checkBoardCard(self, card, usable=False):
        """Show a card from the board in more details

        Keyword arguments:
        card -- Card from the board
        usable -- Boolean, True if the card is usable (default False)
        """
        self.freezeForeground()
        self.cardDisplay.open(card,
                              False,
                              usable=usable)