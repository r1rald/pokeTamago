from obj import Poke
from threading import Thread, Event
import time, sched, sys


if __name__ == "__main__":
    p = Poke()

    s = sched.scheduler(time.time, time.sleep)

    def run(sc):
        p.autosave()
        p.passing_time()
        if p.status["alive"]:
            s.enter(1, 1, run, (sc,))

    s.enter(1, 1, run, (s,))

    breaking = Event()

    t = Thread(target=s.run)
    t.start()

    while p.status['alive']:
        p.run()