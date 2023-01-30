from threading import Thread
from player import Player
import sched
import game
import time
import sys
import os


if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


s = sched.scheduler(time.time, time.sleep)
mg = game.Game()
p = Player()


def run(sc):
    mg.autosave(p)
    p.passing_time()
    s.enter(1, 1, run, (sc,))
    if not mg.run:
        mg.autosave(p)
        sys.exit()


if __name__ == "__main__":
    mg.newGame(p)

    s.enter(1, 1, run, (s,))
    t = Thread(target=s.run)
    t.start()

    while mg.run:
        mg.mainGame(p)
