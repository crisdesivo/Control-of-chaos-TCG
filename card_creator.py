import inspect

unitFormat = """
{name}
HP: {hp}
Primary Type: {primaryType}
Secondary Type: {secondaryType}
Techniques:
    {techniquesFormats}
"""

techniqueFormat = """
    {techniqueName}
        Damage: {techniqueDamage}
        Effects:
            {effectsFormats}
"""

effectFormat = """
            {effectName}
                Timing: {effectTiming}
                Function: {effectFunctionString}
"""


def paralyze(duel):
    possibleTargets = duel.oponentUnits()
    target = duel.selectTarget(possibleTargets)
    target.occupant.paralyzed = True


print(inspect.getsource(paralyze))
