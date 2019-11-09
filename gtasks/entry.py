from queue import Queue
from tui import Terminal
from api import Connection


def parse_state(state):
    return [x[0] for x in state]


class GTasks:
    def __init__(self):
        self.alive = True
        self.q = Queue()
        self.terminal = Terminal(self.q)
        self.connexion = Connection(self.q)

        self.connexion.get_lists()
        self.terminal.loop()

        self.state = []

    def process_events(self, event):
        e, v = event
        if e == 'ITEMS':
            self.state += v
            self.terminal.set_text(parse_state(self.state))
        elif e == Terminal.KEYPRESS:
            if v == 3:
                self.alive = False
                self.terminal.kill()
            elif v == 10:
                self.terminal.scroll_cursor(1)
            elif v == 11:
                self.terminal.scroll_cursor(-1)
            else:
                self.state = [str(v)]
                self.terminal.set_text(self.state)

    def run(self):
        while self.alive:
            self.process_events(self.q.get())


if __name__ == '__main__':
    app = GTasks()
    app.run()
