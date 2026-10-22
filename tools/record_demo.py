"""
Records assets/demo.gif: a real game session, played with real mouse input.

The game runs normally in the main thread. An "autopilot" thread reads the
live game state (where the cards are, whether a menu is open, whose turn it
is...) and moves/clicks the X11 mouse through the XTEST extension, exactly
as a person would. ffmpeg grabs the window and the clip is converted to a GIF.

Needs Linux + Xvfb + ffmpeg + python-xlib (pip install python-xlib):

    xvfb-run -s "-screen 0 1024x768x24" python tools/record_demo.py
"""
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from Xlib import X, display  # noqa: E402
from Xlib.ext import xtest  # noqa: E402

from scr.game_setup import new_duel  # noqa: E402
from ui.constants import CARD_DRAW_WIDTH  # noqa: E402
from ui.duel_gui import DuelGUI  # noqa: E402
from ui.main_menu import MainMenu  # noqa: E402

SEED = 19  # Human goes first with a unit and two Chao energies in hand
OUT_DIR = ROOT / "assets"
TMP_VIDEO = Path("/tmp/coctcg_demo.mp4")

# Fixed spots of the 256x256 game screen (see ui/board_gui.py, card_display.py)
START_BUTTON = (128, 185)
CARD_MENU_BUTTON = (128, 130)   # "Play card" / first technique
FIELD_ENERGIES = (60, 175)
NEXT_TURN = (60, 182)


def own_slot(i):
    return (20 + i * 43 + 21, 132)


def enemy_slot(i):
    return (20 + i * 43 + 21, 70)


class Autopilot:
    """Drives the real mouse pointer in game coordinates."""

    def __init__(self, gui):
        self.gui = gui
        self.d = display.Display()
        self.window = self._find_window()
        geo = self.window.get_geometry()
        pos = self.window.translate_coords(self.d.screen().root, 0, 0)
        self.origin = (-pos.x, -pos.y)
        self.size = (geo.width, geo.height)
        self.scale = geo.width / 256
        self.pos = (128, 230)

    def _find_window(self):
        root = self.d.screen().root
        for _ in range(100):
            for w in root.query_tree().children:
                g = w.get_geometry()
                if g.width >= 256 and w.get_attributes().map_state == X.IsViewable:
                    return w
            time.sleep(0.1)
        raise RuntimeError("Pyxel window not found")

    def _to_screen(self, x, y):
        return (int(self.origin[0] + (x + 0.5) * self.scale),
                int(self.origin[1] + (y + 0.5) * self.scale))

    def move(self, x, y, duration=0.3):
        x0, y0 = self.pos
        steps = max(1, int(duration * 30))
        for k in range(1, steps + 1):
            t = k / steps
            t = t * t * (3 - 2 * t)  # ease in/out
            sx, sy = self._to_screen(x0 + (x - x0) * t, y0 + (y - y0) * t)
            xtest.fake_input(self.d, X.MotionNotify, x=sx, y=sy)
            self.d.sync()
            time.sleep(duration / steps)
        self.pos = (x, y)

    def click(self, x=None, y=None, button=1, pause=0.2):
        if x is not None:
            self.move(x, y)
        time.sleep(0.08)
        xtest.fake_input(self.d, X.ButtonPress, button)
        self.d.sync()
        time.sleep(0.08)
        xtest.fake_input(self.d, X.ButtonRelease, button)
        self.d.sync()
        time.sleep(pause)

    @staticmethod
    def wait(condition, timeout=30):
        end = time.time() + timeout
        while not condition():
            if time.time() > end:
                raise TimeoutError("autopilot waited too long")
            time.sleep(0.05)

    # --- Game-aware helpers -------------------------------------------------
    @property
    def duel(self):
        return self.gui.duel

    def my_turn(self):
        duel = self.duel
        return (duel is not None and duel.turn is not None
                and duel.turn.player == 0 and not self.gui.transition.is_active
                and not duel.endGame)

    def hand_card_x(self, index):
        """x that puts card ``index`` on top (mirrors HandGUI.updateTopIndex:
        with overlapping cards, the card on top depends on the direction
        the pointer comes from)."""
        hand = self.gui.handGUI
        n = len(hand.hand.cards)
        sep = hand.cardSeparation()
        start = (256 - CARD_DRAW_WIDTH - (n - 1) * sep) / 2
        if sep > CARD_DRAW_WIDTH or index <= hand.topIndex:
            return start + index * sep + sep / 2
        return start + CARD_DRAW_WIDTH - sep + index * sep + sep / 2

    def open_hand_card(self, predicate):
        hand = self.gui.handGUI
        index = next(i for i, c in enumerate(hand.hand.cards) if predicate(c))
        self.move(self.hand_card_x(index), 222)
        # Safety net: nudge the pointer until that card is on top
        for _ in range(120):
            time.sleep(0.05)
            if hand.topIndex == index:
                break
            step = 1 if hand.topIndex < index else -1
            self.move(self.pos[0] + step, 222, duration=0.02)
        else:
            raise TimeoutError("could not hover the card")
        time.sleep(0.25)
        self.click()
        self.wait(lambda: not self.gui.cardDisplay.hidden, 3)
        time.sleep(0.8)

    def sweep_hand(self):
        cards = self.gui.handGUI.hand.cards
        for i in range(len(cards)):
            self.move(self.hand_card_x(i), 222, duration=0.12)
            time.sleep(0.08)

    def pick(self, x, y):
        self.wait(lambda: self.gui.boardGUI.findTarget, 5)
        self.move(x, y, duration=0.5)
        time.sleep(0.5)  # let the highlight blink a bit
        self.click(pause=0.4)

    def free_slot(self):
        slots = self.duel.board.units[0]
        return next(i for i, s in enumerate(slots) if s.occupant is None)

    def my_unit_slot(self):
        slots = self.duel.board.units[0]
        return next(i for i, s in enumerate(slots) if s.occupant is not None)

    def enemy_unit_slot(self):
        slots = self.duel.board.units[1]
        return next((i for i, s in enumerate(slots) if s.occupant is not None), None)

    # --- The scripted session ---------------------------------------------
    def play(self):
        is_chao = lambda c: c.cardType == 0 and c.energyType == 4  # noqa: E731
        is_unit = lambda c: c.cardType == 1  # noqa: E731

        time.sleep(1.2)
        self.move(*START_BUTTON, duration=0.6)
        time.sleep(0.5)
        self.click()

        # Turn 1: look at the hand, play a unit and a Chao energy on it
        self.wait(self.my_turn)
        time.sleep(0.6)
        self.sweep_hand()
        self.open_hand_card(is_unit)
        self.click(*CARD_MENU_BUTTON)
        self.pick(*own_slot(self.free_slot()))
        time.sleep(0.4)
        self.open_hand_card(is_chao)
        self.click(*CARD_MENU_BUTTON)
        self.pick(*own_slot(self.my_unit_slot()))
        time.sleep(0.6)
        self.click(*NEXT_TURN)

        # Turn 3: second Chao energy, then attack with Poison Sting
        self.wait(self.my_turn, 60)
        time.sleep(0.8)
        self.open_hand_card(is_chao)
        self.click(*CARD_MENU_BUTTON)
        self.pick(*own_slot(self.my_unit_slot()))
        time.sleep(0.4)
        self.click(*own_slot(self.my_unit_slot()))
        self.wait(lambda: not self.gui.cardDisplay.hidden, 3)
        time.sleep(1.2)
        self.click(*CARD_MENU_BUTTON)
        enemy = self.enemy_unit_slot()
        if enemy is not None:
            self.pick(*enemy_slot(enemy))
        self.wait(self.my_turn, 10)
        self.move(*NEXT_TURN, duration=0.6)
        time.sleep(1.2)
        self.click()

        # Watch the AI answer
        self.wait(self.my_turn, 60)
        time.sleep(1.5)


def record(gui):
    pilot = Autopilot(gui)
    w, h = pilot.size
    ox, oy = pilot.origin
    ffmpeg = subprocess.Popen(
        ["ffmpeg", "-loglevel", "error", "-y", "-f", "x11grab",
         "-framerate", "30", "-video_size", f"{w}x{h}",
         "-i", f"{os.environ['DISPLAY']}+{ox},{oy}",
         "-pix_fmt", "yuv444p", "-crf", "0", str(TMP_VIDEO)],
        stdin=subprocess.PIPE)
    try:
        pilot.play()
    except Exception as error:  # Stop everything instead of hanging
        print(f"Autopilot failed: {error!r}")
        ffmpeg.communicate(b"q")
        os._exit(1)
    ffmpeg.communicate(b"q")
    OUT_DIR.mkdir(exist_ok=True)
    gif = OUT_DIR / "demo.gif"
    # Pyxel draws with 16 colors: nearest-neighbour scaling (2x) and no
    # dithering keep every pixel crisp and the GIF small.
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-i", str(TMP_VIDEO),
         "-vf", "fps=20,scale=512:512:flags=neighbor,split[a][b];"
                "[a]palettegen=max_colors=32:stats_mode=full[p];"
                "[b][p]paletteuse=dither=none",
         str(gif)], check=True)
    print(f"Saved {gif} ({gif.stat().st_size / 1e6:.2f} MB)")
    os._exit(0)


def main():
    gui = DuelGUI()
    threading.Thread(target=record, args=(gui,), daemon=True).start()
    MainMenu().run()
    duel = new_duel(ui=gui, ai_player_index=1, seed=SEED)
    duel.begin()
    gui.show_game_over(duel)


if __name__ == "__main__":
    main()
