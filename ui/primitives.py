"""
Functions used by different classes

Functions:
centeredRects: Converts centered coordinates of a square to regular coordinates
drawChaosLetter: Draws letters with "chaos" style
drawGameLogo: Draws the game logo
drawCard: Draws input card in input location
drawUnitCard: Draws a unit card
drawEnergyCard: Draws an energy card
drawEnergyAmount: Draws the input amount of energies of each kind
drawHP: Displays the amount of hp respective to the max hp
inRect: Given a rect and a point return True if the point is inside the rect
mouseInRect: Given a rect returns True if the mouse cursor is inside
updateWrapper: Wrapper for ui components's update functions


"""
import pyxel
import random
from ui.constants import *
from scr.slot import Slot


def centeredRect(x, y, w, h):
    """Converts centered coordinates of a rectangle to regular coordinates

    Keyword arguments:
    x -- x position of the centered rectangle
    y -- y position of the centered rectangle
    w -- width of the centered rectangle
    h -- height of the centered rectangle
    """
    return (x - int(w/2),
            y - int(h/2),
            w,
            h)


def drawChaosLetter(x, y, u, v, c):
    """Draws letters with "chaos" style

    Keyword arguments:
    x -- x position to draw
    y -- y position to draw
    u -- x position of the letter in asset
    v -- y position of the letter in asset
    c -- Background color of the drawing
    """
    pyxel.load("assets/my_resource.pyxres")
    image = pyxel.image(1)
    for i in range(u, u + 16):
        for j in range(v, v + 16):
            if image.get(i, j) != 0:
                if random.random() < 0.1:
                    color = random.randint(0, 14)
                    if color == 4:
                        color = 15
                    pyxel.pix(x + i - u, y + j - v, color)
                elif random.random() < 0.5:
                    pyxel.pix(x + i - u, y + j - v, c)


def drawGameLogo(x, y, r):
    """Draws the game logo

    Keywords arguments:
    x -- x position of the logo
    y -- y position of the logo
    r -- Radius of the logo
    """
    centerX = x + int(18*2.5) + r
    centerY = y + r
    for i in range(x + int(18*2.5), x + int(18*2.5) + 2*r):
        for j in range(y, y + 2*r):
            if (i-centerX)**2 + (j-centerY)**2 < r**2:
                if random.random() < 0.1:
                    color = random.randint(0, 14)
                    if color == 4:
                        color = 15
                    pyxel.pix(i, j, color)
    pyxel.circb(centerX, centerY, r, 7)
    letterPositionsList = [
        0,
        48,
        80,
        96,
        112,
        48,
        128
    ]
    for i, position in enumerate(letterPositionsList):
        drawChaosLetter(x + i*18, y + 2*r + 6, position, 0, 2)

    letterPositionsList = [
        48,
        144
    ]
    for i, position in enumerate(letterPositionsList):
        drawChaosLetter(
            x + i*18 + 45,
            y + 2*r + 18 + 6 + 3,
            position, 0, 0)

    letterPositionsList = [
        0,
        16,
        32,
        48,
        64
    ]
    for i, position in enumerate(letterPositionsList):
        drawChaosLetter(
            x + i*18 + 18,
            y + 2*r + 36 + 6 + 3 + 3,
            position, 0, 7)

    pyxel.text(x + 27, y + 2*r + 52 + 6 + 6 + 3 + 3, "Trading Card Game", 12)


def drawCard(card, x, y, showEnergies=False):
    """Draws input card in input location

    Keyword arguments:
    card -- Card to draw
    x -- x position to draw the card
    y -- y position to draw the card
    showEnergies -- Boolean, whether to show energies attached (default False)
    """
    if card.cardType == 0:
        drawEnergyCard(card, x, y)
    if card.cardType == 1:
        drawUnitCard(card, x, y, showEnergies=showEnergies)


def drawUnitCard(card, x, y, showEnergies=False):
    """Draws a Unit card

    Keyword arguments:
    card -- Card to draw
    x -- x position to draw the card
    y -- y position to draw the card
    showEnergies -- Boolean, whether to show energies attached (default False)
    """
    pyxel.rect(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEIGHT, 6)
    pyxel.rectb(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEIGHT, 0)
    text = "\n".join(card.name.split())
    pyxel.text(x + 2, y + 2, text, 0)
    drawHP(card.hp, card.maxHP, x, y)
    drawEnergyAmount(x, y + 14, card.energyDeposit.energyCount)


def drawEnergyCard(card, x, y):
    """Draws a Unit card

    Keyword arguments:
    card -- Card to draw
    x -- x position to draw the card
    y -- y position to draw the card
    showEnergies -- Boolean, whether to show energies attached (default False)
    """
    pyxel.rect(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEIGHT,
               ENERGY_COLORS[card.energyType])
    pyxel.rectb(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEIGHT, 0)
    text = "\n".join(card.name.split())
    pyxel.text(x + 2, y + 2, text, 0)
    pyxel.blt(
        x + (CARD_DRAW_WIDTH - ENERGY_SPRITES[card.energyType][2])/2,
        y + 25, 0,
        *ENERGY_SPRITES[card.energyType],
        colkey=4)


def drawEnergyAmount(x, y, energyAmount):
    """Draws an Energy amount

    Keyword arguments:
    x -- x position to draw
    y -- y position to draw
    energyAmount -- List of integers, amount of each energy respectively
    """
    pyxel.rect(x, y, 23, 7, 0)
    for i, count in enumerate(energyAmount):
        pyxel.text(x + 2 + 4*i,
                   y + 1,
                   str(count),
                   ENERGY_COLORS[i])


def drawHP(hp, maxHP, x, y):
    """Displays the amount of hp respective to the max hp

    Keyword arguments:
    hp -- Integer, current hp of the unit
    maxHP -- Integer, max hp of the unit
    x -- x position to draw hp
    y -- y position to draw hp
    """
    r = 3
    sep = 2*r
    startX = x + 4
    startY = y + CARD_DRAW_WIDTH - 7
    for i in range(maxHP):
        if sep*i + 2*r < CARD_DRAW_WIDTH:
            if i < hp:
                pyxel.circ(startX + i*sep, startY, r, col=0)
            else:
                pyxel.circ(startX + i*sep, startY, r, col=7)
                pyxel.circb(startX + i*sep, startY, r, col=0)
        else:
            break
    if i < maxHP - 1:
        for j in range(i, maxHP):
            if sep*(j-i) + 2*r < CARD_DRAW_WIDTH:
                if j < hp:
                    pyxel.circ(startX + (j - i)*sep,
                               startY + 2*r + 2,
                               r,
                               col=0)
                else:
                    pyxel.circ(startX + (j - i)*sep, startY + 2*r + 2, r, col=7)
                    pyxel.circb(startX + (j - i)*sep, startY + 2*r + 2, r, col=0)
            else:
                break
        if j < maxHP - 1:
            for k in range(j, maxHP):
                if k < hp:
                    pyxel.circ(startX + (k - j)*sep,
                               startY + 2*(2*r + 2),
                               r,
                               col=0)
                else:
                    pyxel.circ(startX + (k - j)*sep, startY + 2*(2*r + 2), r, col=7)
                    pyxel.circb(startX + (k - j)*sep, startY + 2*(2*r + 2), r, col=0)


def inRect(rect, x, y):
    """Given a rect and a point return True if the point is inside the rect

    Keyword arguments:
    rect -- Tuple of four elements (x, y, width, height) to define rectangle
    x -- x position of the point
    y -- y position of the point
    """
    inX = x > rect[0] and x < rect[0] + rect[2]
    inY = y > rect[1] and y < rect[1] + rect[3]
    return inX and inY


def mouseInRect(rect):
    """Given a rect returns True if the mouse cursor is inside

    Keyword arguments:
    rect -- Tuple of four elements (x, y, width, height) to define rectangle
    """
    return inRect(rect, pyxel.mouse_x, pyxel.mouse_y)


def updateWrapper(update):
    """Wrapper for ui components's update functions

    Keywords arguments:
    update -- update function to wrap
    """
    def wrappedUpdate(self):
        if not self.frozen:
            ret = update(self)

            if self.freeze:
                self.frozen = True
                self.freeze = False

            return ret
        else:
            if self.unfreeze:
                self.frozen = False
                self.unfreeze = False

        if self.hide:
            self.hidden = True
            self.hide = False

        elif self.unhide:
            self.hidden = False
            self.hide = False
    return wrappedUpdate
