"""
Class DuelGUI: Duel graphic user interface
"""
import pyxel
import time
from ui.card_display import CardDisplay
from ui.hand_gui import HandGUI
from ui.board_gui import BoardGUI
from ui.transitions import TransitionText # Import the new class


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
        pyxel.images[2].load(0, 0, "assets/good_neighbors.png")

        self.duel = None
        self.handGUI = None
        self.boardGUI = None
        self.cardDisplay = None
        # This line must be added to create the transition object instance.
        self.transition = TransitionText(y_pos=120, speed=40, screen_width=pyxel.width, pause_duration=10)

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
        pyxel.cls(4) # Clear screen
        
        # Draw game board and hand first
        if self.boardGUI:
            self.boardGUI.draw()
        if self.handGUI:
            self.handGUI.draw()
        if self.cardDisplay:
            self.cardDisplay.draw()
        
        # Draw the transition on top of everything
        self.transition.draw()
        
        pyxel.flip()

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

    def show_transition(self, text):
        """
        Displays a transition and blocks all other input until it is finished.
        """
        self.transition.start(text)
        while self.transition.is_active:
            start_time = time.time()
            self.transition.update()
            self.draw() # Redraw the entire screen with the moving text
            
            # Maintain 60 FPS
            sleep_time = 1./60. - (time.time() - start_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

    def runTurn(self):
        """
        Runs a turn in the duel until the turn ends or the game ends.
        """
        self.endTurn = False
        while not self.endTurn and not self.duel.endGame:
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