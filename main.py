"""
Control of Chaos TCG - play a duel against the AI.

    python main.py                 # title screen, then you vs the AI
    python main.py --seed 7        # reproducible shuffles / coin flip
    python main.py --hot-seat      # two humans on the same computer
"""
import argparse

from scr.game_setup import new_duel
from ui.duel_gui import DuelGUI
from ui.main_menu import MainMenu


def parse_args():
    parser = argparse.ArgumentParser(description="Control of Chaos TCG")
    parser.add_argument("--seed", type=int, default=None,
                        help="seed for deck shuffles and who goes first")
    parser.add_argument("--hot-seat", action="store_true",
                        help="two human players instead of you vs the AI")
    parser.add_argument("--skip-menu", action="store_true",
                        help="start the duel directly, without the title screen")
    return parser.parse_args()


def main():
    args = parse_args()
    gui = DuelGUI()  # Opens the Pyxel window and loads the assets
    menu = MainMenu()
    game = 0
    while True:
        if not (args.skip_menu and game == 0):
            menu.run()
        seed = None if args.seed is None else args.seed + game
        duel = new_duel(ui=gui,
                        ai_player_index=None if args.hot_seat else 1,
                        seed=seed)
        duel.begin()
        gui.show_game_over(duel)
        game += 1


if __name__ == "__main__":
    main()
