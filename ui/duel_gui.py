"""
Class DuelGUI: Duel graphic user interface
"""
from pathlib import Path

import pyxel
from ui.card_display import CardDisplay
from ui.hand_gui import HandGUI
from ui.board_gui import BoardGUI
from ui.primitives import draw_large_text
from ui.transitions import TransitionText

ASSETS_DIR = Path(__file__).resolve().parent / "assets"


class DuelGUI:
    """
    Duel graphic user interface.

    The rules engine (scr.Duel) calls into this object whenever the human
    player has to decide something (``runTurn``, ``selectTarget``,
    ``selectSlot``) and to announce events (``show_transition``). Each of
    those calls runs its own small Pyxel loop until the player has answered.
    """
    def __init__(self):
        """
        Duel graphic user interface
        """
        pyxel.init(256, 256, title="Control of Chaos TCG", fps=60)
        pyxel.mouse(True)
        pyxel.load(str(ASSETS_DIR / "my_resource.pyxres"))
        pyxel.images[2].load(0, 0, str(ASSETS_DIR / "good_neighbors.png"))

        self.duel = None
        self.handGUI = None
        self.boardGUI = None
        self.cardDisplay = None
        self.endTurn = False
        self.transition = TransitionText(y_pos=120, speed=40, screen_width=pyxel.width, pause_duration=10)

    def addToBackground(self, component):
        """
        Adds the input component to the list of background components
        """
        self.backgroundComponents.append(component)

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

    def initComponents(self, duel, player):
        """
        Initializes the components of the graphic interface

        Keyword arguments:
        duel -- Duel of the interface
        player -- Integer, index (0 or 1), of the player whose hand is shown
        """
        self.backgroundComponents = []
        self.foregroundComponents = []
        self.overlayComponents = []

        self.duel = duel
        self.initHandGUI(player)

        self.boardGUI = BoardGUI(self)
        self.addToForeground(self.boardGUI)

        self.cardDisplay = CardDisplay(self)
        self.addToOverlays(self.cardDisplay)

    def initHandGUI(self, player):
        """
        Initializes the hand graphic interface component

        Keyword arguments:
        player -- Integer, index (0 or 1), of the player whose hand is shown
        """
        self.handGUI = HandGUI(self.duel.players[player].hand)
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

    def draw(self, flip=True):
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

        if flip:
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
        and returns the choice (None if cancelled).

        Keyword arguments:
        possibleTargets -- List of possible targets to choose from
        """
        return self.boardGUI.selectTarget(possibleTargets)

    def selectSlot(self, possibleSlots):
        """Gives the player the ability to choose a slot from a list of slots
        and returns the choice (None if cancelled).

        Keyword arguments:
        possibleTargets -- List of possible targets to choose from
        """
        return self.boardGUI.selectTarget(possibleSlots)

    def show_transition(self, text):
        """
        Displays a transition and blocks all other input until it is finished.
        """
        if self.cardDisplay is not None:
            self.cardDisplay.close()
        self.transition.start(text)
        while self.transition.is_active:
            self.transition.update()
            self.draw()  # pyxel.flip() keeps the loop at the game's fps

    def runTurn(self):
        """
        Runs a turn in the duel until the turn ends or the game ends.
        """
        self.endTurn = False
        while not self.endTurn and not self.duel.endGame:
            self.update()
            self.draw()

    def show_game_over(self, duel):
        """
        Shows the result of the duel until the player clicks.

        Keyword arguments:
        duel -- The finished Duel
        """
        viewer = duel.viewpoint()
        if duel.winner is None:
            title, color = "DRAW", 10
            subtitle = "Nobody can attack anymore"
        elif len(duel.humanPlayers) == 1:
            won = duel.winner == viewer
            title, color = ("VICTORY", 11) if won else ("DEFEAT", 8)
            subtitle = "The opponent ran out of HP" if won else "You ran out of HP"
        else:
            title, color = f"PLAYER {duel.winner + 1} WINS", 11
            subtitle = f"Player {2 - duel.winner} ran out of HP"
        details = f"{duel.turnNumber} turns played"

        def centered(text):
            return (pyxel.width - len(text) * pyxel.FONT_WIDTH) // 2

        if self.cardDisplay is not None:
            self.cardDisplay.close()
        pyxel.flip()
        while not pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.draw(flip=False)
            pyxel.rect(28, 92, 200, 64, 0)
            pyxel.rectb(28, 92, 200, 64, pyxel.frame_count // 8 % 16)
            draw_large_text(centered(title), 102, title, color)
            pyxel.text(centered(subtitle), 118, subtitle, 7)
            pyxel.text(centered(details), 128, details, 6)
            hint = "Click to return to the title screen"
            pyxel.text(centered(hint), 144, hint, 5)
            pyxel.flip()
        pyxel.flip()

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
