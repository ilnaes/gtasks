from eventbox import EventBox
from tui import Terminal
from api import Connection


def parse_state(state):
    return [x[0] for x in state]


def run():
    eb = EventBox()
    terminal = Terminal(eb)
    connexion = Connection(eb)

    connexion.get_lists()
    terminal.loop()
    alive = True

    state = []

    def _callback(events):
        nonlocal alive, state

        while events:
            e, v = events.pop()
            if e == 'ITEMS':
                state += v
                terminal.set_text(parse_state(state))
            elif e == Terminal.KEYPRESS:
                if v == 3:
                    alive = False
                    terminal.kill()
                elif v == 10:
                    # down
                    terminal.scroll_cursor(1)
                elif v == 11:
                    # up
                    terminal.scroll_cursor(-1)
                else:
                    state = [str(v)]
                    terminal.set_text(state)

    while alive:
        eb.wait(_callback)


if __name__ == '__main__':
    run()
