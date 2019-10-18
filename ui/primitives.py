import pyxel
import random
from ui.constants import *


def centeredRect(x, y, w, h):
    return (x - int(w/2),
            y - int(h/2),
            w,
            h)


def drawChaosLetter(x, y, u, v, c):
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


def drawCard(card, x, y):
    if card.cardType == 0:
        drawEnergyCard(card, x, y)
    if card.cardType == 1:
        drawUnitCard(card, x, y)


def drawUnitCard(card, x, y):
    pyxel.rect(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEIGHT, 6)
    pyxel.rectb(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEIGHT, 0)
    text = "\n".join(card.name.split())
    pyxel.text(x + 2, y + 2, text, 0)
    drawHP(card.hp, card.maxHP, x, y)


def drawHP(hp, maxHP, x, y):
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


def drawEnergyCard(card, x, y):
    pyxel.rect(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEIGHT,
               ENERGY_COLORS[card.energyType])
    pyxel.rectb(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEIGHT, 0)
    text = "\n".join(card.name.split())
    pyxel.text(x + 2, y + 2, text, 0)
    pyxel.blt(
        x + 12,
        y + 25, 0,
        *ENERGY_SPRITES[card.energyType],
        colkey=4)


def inRect(rect, x, y):
    inX = x > rect[0] and x < rect[0] + rect[2]
    inY = y > rect[1] and y < rect[1] + rect[3]
    return inX and inY
