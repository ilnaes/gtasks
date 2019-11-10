import threading
import time
import unittest
from datetime import datetime
from unittest.mock import patch
from pygtasks.core import PygTasks


def sleep():
    time.sleep(0.01)


class TestCore(unittest.TestCase):

    @patch('pygtasks.core.Connection')
    @patch('pygtasks.core.Terminal')
    def setUp(self, mox_terminal, mox_cxn):
        self.app = PygTasks()
        threading.Thread(target=self.app.run, daemon=True).start()

    def tearDown(self):
        pass

    def test_start(self):
        """ Verify app's lists properly initializes """

        lists = [['', 'a', None], ['qiwe', 's', None], ['aa', 'c', None]]
        self.app.q.put(('LISTS', lists))
        sleep()
        self.assertEqual(self.app.get_length(), 3)

    def test_tasks(self):
        """ Verify adding tasks adds the right amount """
        lists = [['', 'a', None], ['qiwe', 's', None], ['aa', 'c', None]]
        task1 = [['', '', datetime.now()], ['', '', datetime.now()]]
        task2 = [['', '', datetime.now()]]

        self.app.q.put(('LISTS', lists))
        self.app.q.put(('TASKS', ('a', task1)))
        sleep()

        self.assertEqual(len(self.app.parse_state()), len(lists) + len(task1))
        self.assertEqual(self.app.lists[0][2], task1)

        self.app.q.put(('TASKS', ('b', task2)))
        sleep()

        self.assertEqual(len(self.app.parse_state()), len(lists) + len(task1))

        self.app.q.put(('TASKS', ('s', task2)))
        sleep()
        self.assertEqual(len(self.app.parse_state()), len(lists) + len(task1) + len(task2))
        self.assertEqual(self.app.lists[1][2], task2)

    def test_cursor(self):
        """ Verify cursor stay in bounds """

        lists = [['', 'as', None], ['qiwe', 'asd', None], ['aa', 'q23', None]]
        self.app.q.put(('LISTS', lists))

        for i in range(100):
            self.app.q.put((2, 106))

        sleep()
        self.assertEqual(self.app.cursor, 2)

        for i in range(100):
            self.app.q.put((2, 107))

        sleep()
        self.assertEqual(self.app.cursor, 0)
