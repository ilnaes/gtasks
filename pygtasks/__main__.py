from .core import PygTasks
import sys
import os

path = None
if len(sys.argv) > 1:
    path = os.getcwd() + '/' + sys.argv[1]
app = PygTasks(path)
app.run()
