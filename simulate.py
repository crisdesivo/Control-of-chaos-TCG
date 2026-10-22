"""
Headless AI-vs-AI simulator.

Plays many duels with the real rules engine (no window, no Pyxel) and prints
balance statistics: win rate per deck, first-player advantage, draws and game
length. Useful to check that a rule or card change doesn't break the game.

    python simulate.py --games 1000 --seed 0
"""
import argparse
import statistics
from collections import Counter

from scr.card_factory import CardFactory
from scr.game_setup import CARDS_PATH, new_duel


def run(games, seed=0, max_turns=500):
    """Plays ``games`` AI-vs-AI duels and returns a list of result dicts."""
    factory = CardFactory(CARDS_PATH)
    results = []
    for i in range(games):
        duel = new_duel(seed=seed + i, max_turns=max_turns, factory=factory)
        winner = duel.begin()
        results.append({
            "winner": winner,
            "first": duel.firstPlayer,
            "turns": duel.turnNumber,
            "timeout": winner is None and duel.turnNumber >= max_turns,
        })
    return results


def summarize(results):
    """Prints a small report of the simulated duels."""
    n = len(results)
    winners = Counter(r["winner"] for r in results)
    decided = [r for r in results if r["winner"] is not None]
    first_wins = sum(r["winner"] == r["first"] for r in decided)
    timeouts = sum(r["timeout"] for r in results)
    turns = [r["turns"] for r in decided]

    def pct(k, total):
        return f"{100 * k / total:5.1f}%" if total else "  n/a"

    print(f"Duels simulated           {n}")
    print(f"Player 1 (U01 deck) wins  {winners[0]:5d}  {pct(winners[0], n)}")
    print(f"Player 2 (U02 deck) wins  {winners[1]:5d}  {pct(winners[1], n)}")
    print(f"Draws                     {winners[None]:5d}  {pct(winners[None], n)}"
          f"  (turn limit: {timeouts})")
    print(f"First player wins         {first_wins:5d}  "
          f"{pct(first_wins, len(decided))} of decided duels")
    if turns:
        print(f"Turns per decided duel    mean {statistics.mean(turns):.1f}, "
              f"median {statistics.median(turns):.0f}, "
              f"min {min(turns)}, max {max(turns)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--games", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-turns", type=int, default=500)
    args = parser.parse_args()
    summarize(run(args.games, args.seed, args.max_turns))


if __name__ == "__main__":
    main()
