# PygTasks

This is a simple terminal application for Google Tasks.  You can view, create, complete, and delete tasks in your tasklists.

# Installation

You'll need setuptools, which you get get from pip.  Once you have that, type the following in the main directory

```sh
python setup.py install
```

# Usage

```sh
pygtasks [ credentials.json ]
```

The first time you use pygtasks, you must supply it with the path of your credentials json file (you can search for ways to get that).  You will be taken through the Google API authentication process on a browser, which will write your token in ~/.pyenv afterwards.  In subsequent launches, you will not need to provide any arguments.

The following commands are available:

* `j/k` to navigate down/up respectively
* `<Space>` to expand/contract a tasklist
* `c` to complete a highlighted task
* `x` to delete a highlighted task/tasklist
* `t` to add a new task to a tasklist
* `l` to add a new tasklist
* `q` to quit
* `<Ctrl-c>` to abort adding a task
