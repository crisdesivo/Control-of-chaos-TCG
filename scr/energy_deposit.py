"""
Class EnergyDeposit: Handles the logic of energy reserves
"""


class EnergyDeposit:
    """Handles the logic of energy reserves
    """
    def __init__(self, parent):
        """Handles the logic of energy reserves

        Keyword arguments:
        parent -- Location of the energy deposit
        """
        self.parent = parent
        self.energies = []
        self.name = "Energy deposit"
        self.energyCount = [0, 0, 0, 0, 0]

    def attach(self, card):
        """Adds an energy card to the reserve

        Keyword arguments:
        card -- Energy card to add to the reserve
        """
        assert card.cardType == 0
        self.energies.append(card)
        card.parent = self
        self.energyCount[card.energyType] += 1

    def remove(self, energyAmount):
        """Removes a list of energies amounts from itself

        Keyword arguments:
        energyAmount -- List of integers, amount of each energy respectively
        """
        for energyType in range(5):
            amount = energyAmount[energyType]
            assert self.energyCount[energyType] >= amount
            self.energyCount[energyType] -= amount
            for _ in range(amount):
                for card in self.energies:
                    if card.energyType == energyType:
                        self.energies.remove(card)
                        break
