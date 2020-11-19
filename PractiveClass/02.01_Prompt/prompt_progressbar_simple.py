import time
from prompt_toolkit.shortcuts import ProgressBar

with ProgressBar() as bar:
    for i in bar(range(120)):
        time.sleep(.05)
