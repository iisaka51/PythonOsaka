from notedb import *
from pprint import pprint

notes = Note.select(Note.text, Note.created)

v1 = [e for e in notes.tuples()]

# pprint(v1)
