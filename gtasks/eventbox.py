from threading import Condition


class EventBox:
    def __init__(self):
        self.c = Condition()
        self.events = {}
