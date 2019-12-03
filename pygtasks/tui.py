import string
import sys
import tty
import termios
import threading


def csi(s):
    sys.stdout.write('\x1b[' + s)


class Terminal:
    KEYPRESS = 2
    HEIGHT = 10

    def __init__(self, q):
        self.global_events = q
        self.text = []
        self.top = 0
        self.cursor = 0
        self.input = ''
        self.prompt = ''
        self.lock = threading.Lock()
        self.alive = True

        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(sys.stdin)
        csi('?25l')

    def get_prompt(self, s, q):
        self.prompt = '> ' + s
        self.input = ''
        self.refresh(True)

        while True:
            e, v = q.get()
            if e == Terminal.KEYPRESS:
                if v == 3:
                    self.input = ''
                    self.prompt = ''
                    self.refresh(False)
                    return None
                elif v == 13:
                    tmp = self.input
                    self.input = ''
                    self.prompt = ''
                    self.refresh(False)
                    return tmp
                elif v == 127:
                    self.input = self.input[:-1]
                    self.refresh(True)
                elif chr(v) in string.printable:
                    self.input += chr(v)
                    self.refresh(True)

    def kill(self):
        with self.lock:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            csi('?25h')
            self.clear()
            self.alive = False

    def clear(self):
        csi(str(Terminal.HEIGHT) + 'A')
        csi('G')
        csi('J')

    def scroll_cursor(self, n):
        with self.lock:
            self.cursor += n
            if self.top + Terminal.HEIGHT <= self.cursor:
                self.top = self.cursor - Terminal.HEIGHT + 1
            elif self.top > self.cursor:
                self.top = self.cursor
        self.refresh(False)

    def print_text(self, cursor):
        with self.lock:
            if cursor:
                csi('?25h')
            else:
                csi('?25l')

            for i in range(Terminal.HEIGHT):
                if self.top + i < len(self.text):
                    if self.top + i == self.cursor:
                        sys.stdout.write('\u001b[37;1m')
                        sys.stdout.write(self.text[self.top + i])
                        sys.stdout.write('\u001b[0m\r\n')
                    else:
                        sys.stdout.write(self.text[self.top + i] + '\r\n')

            for i in range(self.top + Terminal.HEIGHT - len(self.text)):
                sys.stdout.write('\r\n')

            csi('37;1m')
            sys.stdout.write(self.prompt)
            csi('0m')
            sys.stdout.write(self.input)
            sys.stdout.flush()

    def refresh(self, cursor):
        self.clear()
        self.print_text(cursor)

    def set_text(self, text):
        with self.lock:
            self.text = text
        self.refresh(False)

    def set_input(self, s):
        with self.lock:
            self.input = s
        self.refresh(False)

    def scroll(self, n):
        with self.lock:
            if self.top + n < len(self.text) and self.top + n >= 0:
                self.top += n
        self.refresh(False)

    def loop(self):
        # self.drawloop()
        self.print_text(False)

        def _loop():
            while True:
                ch = sys.stdin.read(1)
                self.global_events.put((Terminal.KEYPRESS, ord(ch)))

        threading.Thread(target=_loop, daemon=True).start()
