from threading import Thread
from classes import Player
import mainGame
import time
import sched
import sys


p = Player()
mg = mainGame.Gameplay()
s = sched.scheduler(time.time, time.sleep)


def run(sc):
    p.autosave()
    p.passing_time()
    s.enter(1, 1, run, (sc,))
    if not p.run:
        p.autosave()
        sys.exit()


if __name__ == "__main__":

    mg.newGame(p)

    s.enter(1, 1, run, (s,))
    t = Thread(target=s.run)
    t.start()

    while mg.run:
        mg.mainGame(p)
