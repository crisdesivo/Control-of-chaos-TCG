YES_CHOICES = [
    "yes",
    "Yes",
    "YES",
    "y",
    "Y",
    "s",
    "S",
    "SI",
    "Si",
    "si"
]
NO_CHOICES = [
    "no",
    "No",
    "NO",
    "n",
    "N"
]


def presentOptions(options=[],
                   nameFunction=lambda x: "None",
                   cancelNumber=None,
                   cancel=-1):
    if cancelNumber is not None:
        print(f"{cancelNumber}: Cancel")
    for i, option in enumerate(options):
        print(f"{i}: {nameFunction(option)}")
    numberOptions = list(range(len(options)))
    if cancelNumber is not None:
        numberOptions = [cancelNumber] + numberOptions
    choice = ""

    while choice not in numberOptions and not isinstance(choice, int):
        print(f"Choose a number from {numberOptions}")
        choice = input("Selection: ")
        try:
            choice = int(choice)
        except ValueError:
            print("Choose an integer")

    if choice == cancelNumber:
        return cancel
    return options[choice]


class UserInterface:
    match = None

    def startGameMatch(self, match):
        self.match = match

    def selectTarget(self, possibleTargets):
        return presentOptions(
            options=[slot.occupant for slot in possibleTargets],
            nameFunction=lambda x: x.name,
            cancelNumber=-1)

    def selectSlot(self, possibleSlots):
        return presentOptions(
            options=possibleSlots,
            nameFunction=lambda x: x.name,
            cancelNumber=-1)

    def selectTechnique(self, unit):
        return presentOptions(
            options=unit.techniques,
            nameFunction=lambda x: x.name,
            cancelNumber=-1,
            cancel=None)

    def selectToCheck(self, cards):
        return presentOptions(
            options=cards,
            nameFunction=lambda x: x.name,
            cancelNumber=-1)

    def selectPlay(self, player):
        optionNames = [
            f"End Turn",
            f"Look at hand",
            f"Look at my units",
            f"Look at enemy units"
            f"Look at my energies",
            f"Look at enemy energies",
            f"Look at my graveyard",
            f"Look at enemy graveyard",
            f"Look at game info"
        ]
        options = list(range(8))
        choice = presentOptions(
            options=options,
            nameFunction=lambda x: optionNames[x],
            cancelNumber=None
        )
        print(f"Selected choice {choice}")
        if choice == 0:
            return True
        elif choice == 1:
            print("Choose 1")
            hand = self.match.players[player].hand
            cards = hand.cards
            cardChoice = None
            while cardChoice != -1:
                cardChoice = self.selectToCheck(cards)
                if cardChoice != -1:
                    self.checkHandCard(cardChoice)
            print()
            self.selectPlay(player)
        elif choice == 2:
            cards = [slot.occupant for slot in self.match.board.units[player]]
            cards = [card for card in cards if card is not None]
            cardChoice = self.selectToCheck(cards)
            if cardChoice == -1:
                self.selectPlay(player)
            else:
                self.checkUnitCard(cardChoice)
        elif choice == 3:
            cards = [slot.occupant for slot in self.match.board.units[1-player]]
            cards = [card for card in cards if card is not None]
            cardChoice = self.selectToCheck(cards)
            if cardChoice == -1:
                self.selectPlay(player)
            else:
                self.checkEnemyUnitCard(cardChoice)

    def swapPlayers(self):
        pass

    def checkHandCard(self, card):
        print("")
        print(card.name)
        print("")
        if card.playable(self.match):
            choice = input("Play this card? (y/N) ")
            if choice in YES_CHOICES:
                card.play(self.match)
    
    def checkEnemyUnitCard(self, card):
        print()
        print(card.name)
        print()
    
    def checkUnitCard(self, card):
        print()
        print(card.name)
        print()
        if card.active:
            choice = input("Use this card? (y/N) ")
            if choice in YES_CHOICES:
                card.use(self.match)


