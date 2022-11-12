from obj import Poke
from threading import Thread
import time
import sched
import sys


def main():
    p = Poke()

    s = sched.scheduler(time.time, time.sleep)

    def run(sc):
        p.autosave()
        p.passing_time()
        s.enter(1, 1, run, (sc,))
        if not p.run:
            p.autosave()
            sys.exit()

    s.enter(1, 1, run, (s,))
    t = Thread(target=s.run)
    t.start()

    while p.run:
        p.run()


if __name__ == "__main__":
    main()
