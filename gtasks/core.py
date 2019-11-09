from queue import Queue
import datetime as dt
from tui import Terminal
from api import Connection


class GTasks:
    def __init__(self):
        self.alive = True
        self.q = Queue()
        self.terminal = Terminal(self.q)
        self.connexion = Connection(self.q)
        self.cursor = 0

        self.connexion.get_lists()
        self.terminal.loop()

        self.state = []

    def parse_state(self):
        res = []
        now = dt.datetime.now()

        for t, _, l in self.state:
            if l is None:
                res.append('+ ' + t)
            else:
                res.append('- ' + t)
                for y, _, d in l:
                    dfmt = d.strftime('%m/%d/%Y')

                    if d < now:
                        line = u'  \033[31m{0} -- {1}\033[0m'.format(dfmt, y)
                    else:
                        line = u'  \033[32m{0} -- {1}\033[0m'.format(dfmt, y)

                    res.append(line)
                    # res.append('  ' + y)

        return res

    def scroll_cursor(self, n):
        if self.cursor + n >= 0 and self.cursor + n < self.get_length():
            self.cursor += n
            self.terminal.scroll_cursor(n)

    def get_item(self):
        i = 0
        for x in self.state:
            if self.cursor == i:
                return True, x

            i += 1
            _, _, desc = x
            if desc is not None:
                for y in desc:
                    if self.cursor == i:
                        return False, y
                    i += 1

    def get_length(self):
        res = len(self.state)
        for _, _, x in self.state:
            res += 0 if x is None else len(x)
        return res

    def toggle_list(self):
        task, item = self.get_item()

        if task:
            if item[2] is None:
                self.connexion.get_tasks(item[1])
            else:
                item[2] = None
                self.terminal.set_text(self.parse_state())
        else:
            self.terminal.input = item[0]
            self.terminal.refresh()

    def process_events(self, event):
        e, v = event
        if e == 'LISTS':
            self.state = v
            self.terminal.set_text(self.parse_state())
        elif e == 'TASKS':
            for l in self.state:
                if l[1] == v[0]:
                    l[2] = v[1]
            self.terminal.set_text(self.parse_state())
        elif e == Terminal.KEYPRESS:
            if v == 3 or v == 113:
                self.alive = False
                self.terminal.kill()
            elif v == 10:
                self.scroll_cursor(1)
            elif v == 11:
                self.scroll_cursor(-1)
            elif v == 32:
                self.toggle_list()
            elif v == 97:
                a = self.terminal.get_prompt("Input title: ", self.q)
                if a is not None:
                    self.terminal.set_input(a)
            else:
                self.terminal.set_input(str(v))

    def run(self):
        while self.alive:
            self.process_events(self.q.get())


if __name__ == '__main__':
    app = GTasks()
    app.run()
