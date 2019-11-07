from threading import Condition


class EventBox:
    def __init__(self):
        self.c = Condition()
        self.events = {}

    def __set__(self, event):
        self.c.acquire()
        self.c.release()
