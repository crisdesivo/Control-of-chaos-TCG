import pyxel
from ui.constants import *


def centeredRect(x, y, w, h):
    return (x - int(w/2),
            y - int(h/2),
            w,
            h)


def drawCard(card, x, y):
    if card.cardType == 0:
        drawEnergyCard(card, x, y)
    if card.cardType == 1:
        drawUnitCard(card, x, y)


def drawUnitCard(card, x, y):
    pyxel.rect(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEiGHT, 6)
    pyxel.rectb(x, y, CARD_DRAW_WIDTH, CARD_DRAW_HEiGHT, 0)
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
