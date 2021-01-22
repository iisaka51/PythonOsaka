from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.formatted_text import HTML
import time

title = HTML(f'Downloading <style bg="yellow" fg="black">4 files...</style>')
label = HTML('<ansired>some file</ansired>: ')

with ProgressBar(title=title) as pb:
    for i in pb(range(800), label=label):
        time.sleep(.01)
