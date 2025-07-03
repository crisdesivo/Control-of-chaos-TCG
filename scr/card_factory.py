import json
from scr.card import Unit, Energy
from scr.technique import Technique
from scr.effect import Effect

# --- Effect Functions ---
# These functions are mapped by name from the JSON file.
def paralyze(duel, target):
    if target is not None:
        target.paralyzed = True

def poison(duel, target):
    if target is not None:
        target.poisoned = True

EFFECT_FUNCTIONS = {
    'paralyze': paralyze,
    'poison': poison
}
# --- End Effect Functions ---

class CardFactory:
    """Creates instances of cards from a central data file."""
    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            self.data = json.load(f)
        self._build_effect_map()

    def _build_effect_map(self):
        """Pre-builds Effect objects for easy lookup."""
        self.effects = {}
        for id, data in self.data['effects'].items():
            func = EFFECT_FUNCTIONS.get(data['function'])
            if func:
                self.effects[id] = Effect(func, data['timing'])

    def _create_technique(self, tech_id):
        """Creates a single Technique instance."""
        tech_data = self.data['techniques'][tech_id]
        effects = [self.effects[eid] for eid in tech_data.get('effects', [])]
        return Technique(
            name=tech_data['name'],
            description=tech_data['description'],
            damage=tech_data.get('damage', 1),
            cost=tech_data['cost'],
            effects=effects
        )

    def create_card(self, card_id, parent_deck):
        """Creates a fresh instance of a card by its ID."""
        if card_id in self.data['units']:
            card_data = self.data['units'][card_id]
            techniques = [self._create_technique(tid) for tid in card_data.get('techniques', [])]
            return Unit(
                parent=parent_deck,
                name=card_data['name'],
                hp=card_data['hp'],
                primaryType=card_data['primaryType'],
                secondaryType=card_data['secondaryType'],
                techniques=techniques
            )
        elif card_id in self.data['energies']:
            card_data = self.data['energies'][card_id]
            return Energy(
                parent=parent_deck,
                energyType=card_data['energyType']
            )
        raise ValueError(f"Card ID {card_id} not found in database.")