class Technique:
    """Handles the logic of techniques
    """
    def __init__(
            self,
            effects=[],
            damage=1,
            name="",
            description="",
            cost=[0, 0, 0, 0, 0]):
        """Handles the logic of techniques

        Keywords arguments:
        effects -- List of Effects the technique produces (default [])
        damage -- Integer, amount of damage the technique does (default 1)
        name -- String, name of the technique (default "")
        description -- String, description of the card (default "")
        cost -- List of 5 Integers, the cost of each type of energy
        (default [0,0,0,0,0])
        """
        self.effects = effects
        self.damage = damage
        self.name = name
        self.description = description
        self.cost = cost

    def play(self, duel, user):
        """Executes the technique

        Keyword arguments:
        duel -- Current Duel
        user -- Unit that performs the technique
        """
        # payCost = duel.selectEnergies
        print(f"To pay: {self.cost}")
        energiesAttached = user.energyDeposit.energyCount
        print(f"Energies attached: {energiesAttached}")
        player = user.parent.player
        energiesInField = duel.board.energies[player].occupant.energyCount
        print(f"Energies in field: {energiesInField}")
        minEnergiesFromField = [0, 0, 0, 0, 0]
        maxEnergiesFromField = self.cost
        hasEnough = True
        for i in range(5):
            if self.cost[i] > energiesAttached[i]:
                print(i)
                minEnergiesFromField[i] = self.cost[i] - energiesAttached[i]
                if minEnergiesFromField[i] > energiesInField[i]:
                    hasEnough = False
                    break
                else:
                    print(self.cost[i], energiesAttached[i])
            maxEnergiesFromField = min(self.cost[i], energiesInField[i])
        print(f"Min energies from field: {minEnergiesFromField}")
        print(f"Max energies from field: {maxEnergiesFromField}")

        if hasEnough:
            print("has enough energies")
            duringAttackEffects = []
            for effect in self.effects:
                if effect.timing == 0:
                    effect.activate(duel)
                elif effect.timing == 1:
                    duringAttackEffects.append(effect)
            if self.damage > 0:
                duel.turn.addAttack(self, user, duringAttackEffects)
            user.canAttack = False
            return True
        else:
            print("Not enough energies")
            return False

    def hasEnoughEnergies(self, user):
        """Checks if the user has enough energies

        Keywords arguments:
        user -- Unit
        """
        duel = user.duel
        energiesAttached = user.energyDeposit.energyCount
        player = user.parent.player
        energiesInField = duel.board.energies[player].occupant.energyCount
        minEnergiesFromField = [0, 0, 0, 0, 0]
        hasEnough = True
        for i in range(5):
            if self.cost[i] > energiesAttached[i]:
                minEnergiesFromField[i] = self.cost[i] - energiesAttached[i]
                if minEnergiesFromField[i] > energiesInField[i]:
                    hasEnough = False
                    break
        return hasEnough
