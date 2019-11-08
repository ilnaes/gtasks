from threading import Condition


class EventBox:
    def __init__(self):
        self.c = Condition()
        self.events = []

    def set(self, event):
        with self.c:
            self.events.append(event)
            self.c.notify_all()

    def wait(self, callback):
        with self.c:
            while not self.events:
                self.c.wait()

            callback(self.events)

