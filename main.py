from Data.player import Player
from threading import Thread
from sched import scheduler
from Data.game import Game
import time as t
import sys
import os


if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


s = scheduler(t.time, t.sleep)
t = Thread(target=s.run)
g = Game()
p = Player()

def run(sc):
    g.autosave(p)
    p.passing_time()
    s.enter(1, 1, run, (sc,))
    if not g.run:
        g.autosave(p)
        sys.exit()

if __name__ == "__main__":
    g.newGame(p)

    s.enter(1, 1, run, (s,))
    t.start()

    while g.run:
        g.mainGame(p)
