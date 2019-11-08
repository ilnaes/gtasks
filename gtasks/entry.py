from eventbox import EventBox
from tui import Terminal


def run():
    eb = EventBox()
    terminal = Terminal(eb)
    terminal.loop()
    alive = True

    def _callback(events):
        nonlocal alive

        while events:
            e, v = events.pop()
            if e == Terminal.KEYPRESS:
                if v == 3:
                    alive = False
                    terminal.kill()
                else:
                    terminal.local_events.set((e, v))

    while alive:
        eb.wait(_callback)


if __name__ == '__main__':
    run()
