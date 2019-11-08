import sys
import tty
import termios
import threading
from eventbox import EventBox


def csi(s):
    sys.stdout.write('\x1b['+s)


class Terminal:
    KILL = 1
    KEYPRESS = 2
    HEIGHT = 10

    def __init__(self, eventbox):
        self.local_events = EventBox()
        self.global_events = eventbox
        self.text = []
        self.cy = 0
        self.cx = 0
        self.input = ''
        self.lock = threading.Lock()
        self.alive = True

        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(sys.stdin)
        csi('s')

    def kill(self):
        with self.lock:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            self.clear()
            self.alive = False

    def clear(self):
        csi('u')
        csi('J')

    def print_text(self):
        for i in range(Terminal.HEIGHT):
            if self.cy + i < len(self.text):
                sys.stdout.write(self.text[self.cy+i] + '\r\n')

        for i in range(self.cy + Terminal.HEIGHT - len(self.text)):
            sys.stdout.write('\r\n')

    def drawloop(self):
        def _callback(events):
            while events:
                e, v = events.pop()

                with self.lock:
                    if self.alive:
                        if e == Terminal.KEYPRESS:
                            self.text.append(str(v))
                            if len(self.text) > Terminal.HEIGHT:
                                self.cy += 1

                            self.clear()
                            self.print_text()

        def _loop():
            self.print_text()

            while True:
                self.local_events.wait(_callback)

        threading.Thread(target=_loop, daemon=True).start()

    def loop(self):
        self.drawloop()

        def _loop():
            while True:
                ch = sys.stdin.read(1)
                self.global_events.set((Terminal.KEYPRESS, ord(ch)))

        threading.Thread(target=_loop, daemon=True).start()
