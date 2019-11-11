import sys
import os
from .core import PygTasks


def main():
    path = None
    if len(sys.argv) > 1:
        path = os.getcwd() + '/' + sys.argv[1]
    app = PygTasks(path)
    app.run()


if __name__ == '__main__':
    main()
