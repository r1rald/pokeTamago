from obj import Poke
from threading import Thread
import time, sched


if __name__ == "__main__":
    p = Poke()

    s = sched.scheduler(time.time, time.sleep)

    def run(sc):
        p.autosave()
        p.passing_time()
        if p.status["alive"]:
            s.enter(1, 1, run, (sc,))

    s.enter(1, 1, run, (s,))

    t = Thread(target=s.run)
    t.start()

    while p.status['alive']:
        p.run()