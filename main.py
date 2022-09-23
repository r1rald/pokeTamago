from obj import Poke
from threading import Thread
import time, sched, sys


if __name__ == "__main__":
    p = Poke()

    s = sched.scheduler(time.time, time.sleep)

    def run(sc):
        p.autosave()
        p.passing_time()
        s.enter(1, 1, run, (sc,))
        if p.run is False:
            p.autosave()
            sys.exit()

    s.enter(1, 1, run, (s,))
    t = Thread(target=s.run)
    t.start()

    while True:
        p.run()
