from obj import Poke
from threading import Thread
import time, sched, sys


if __name__ == "__main__":
    p = Poke()

    s = sched.scheduler(time.time, time.sleep)

    def run(sc):
        p.autosave()
        p.passing_time()
        if p.status["alive"]:
            s.enter(1, 1, run, (sc,))
        if p.run is False:
            sys.exit()

    s.enter(1, 1, run, (s,))
    t = Thread(target=s.run)
    t.start()

    while p.status['alive']:
        p.run()
