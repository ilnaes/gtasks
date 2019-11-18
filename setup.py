from setuptools import setup
import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'

install_requires = []  # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]

if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(name='pygtasks',
      version='0.1.0',
      packages=['pygtasks'],
      install_requires=install_requires,
      entry_points={'console_scripts': ['pygtasks = pygtasks.__main__:main']})
