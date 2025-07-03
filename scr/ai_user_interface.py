"""
Class AI_UserInterface: Provides an interface for an AI opponent.
"""


class AI_UserInterface:
    """
    Provides an interface for an AI opponent, making decisions based on
    pre-defined rules.
    """
    def __init__(self, duel):
        self.duel = duel

    def selectSlot(self, possibleSlots):
        """AI logic for selecting a slot to play a unit."""
        if possibleSlots:
            # Simplest logic: play in the first available slot.
            return possibleSlots[0]
        return None

    def selectTarget(self, possibleTargets):
        """AI logic for selecting a target for an attack or energy."""
        if not possibleTargets:
            return None

        # Determine if targeting is for a friendly card (like energy)
        is_friendly_target = possibleTargets[0].player == self.duel.turn.player

        if is_friendly_target:
            # Filter for units, which have maxHP
            unit_targets = [s for s in possibleTargets if hasattr(s.occupant, 'maxHP')]
            
            # If there are units, prioritize placing energy on the one with the most HP.
            if unit_targets:
                best_target = max(unit_targets, key=lambda s: s.occupant.maxHP)
                return best_target
            # If no units, the only other target must be the main energy deposit.
            else:
                return possibleTargets[0]

        # If targeting is for an attack (target is an enemy unit)
        else:
            # Prioritize attacking the unit with the lowest HP to remove threats.
            best_target = min(possibleTargets, key=lambda s: s.occupant.hp)
            return best_target

    def runTurn(self):
        """Executes the AI's turn based on a sequence of priorities."""
        player = self.duel.players[self.duel.turn.player]
        hand = player.hand.cards

        # Priority 1: Play an energy card if possible.
        for card in list(hand): # Iterate over a copy as the list may be modified
            if card.cardType == 0 and card.playable(self.duel):
                card.play(self.duel)
                break  # Play only one energy per turn

        # Priority 2: Play a unit card if possible.
        for card in list(hand):
            if card.cardType == 1 and card.playable(self.duel):
                card.play(self.duel)
                break  # Play only one unit per turn

        # Priority 3: Use a technique if possible.
        for slot in self.duel.playerUnits():
            unit = slot.occupant
            if unit and unit.canAttack:
                # Prioritize techniques that can be afforded
                affordable_techs = [t for t in unit.techniques if t.hasEnoughEnergies(unit, self.duel)]
                if affordable_techs:
                    # Simplest logic: use the first affordable technique.
                    if affordable_techs[0].play(self.duel, unit):
                        # An attack was successfully made.
                        self.duel.turn.endTurn = True
                        return

        # If no other action was taken, end the turn.
        self.duel.turn.endTurn = True