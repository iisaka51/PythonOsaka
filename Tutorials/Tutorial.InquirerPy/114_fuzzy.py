from contextlib import ExitStack
from pathlib import Path

from InquirerPy import inquirer, prompt

_WORDFILE_ = 'sample.txt'
def get_choices(_):
    p = Path.cwd().joinpath(_WORDFILE_)
    choices = []

    with ExitStack() as stack:
        if not p.exists():
            raise Exception('%s: wordfile missing!', _WORDFILE_)
        else:
            file = stack.enter_context(p.open("r"))
        for line in file.readlines():
            choices.append(line[:-1])
    return choices

action = inquirer.fuzzy(
    message="Select actions:",
    choices=["hello", "weather", "what", "whoa", "hey", "yo"],
    default="he",
    max_height="70%",
).execute()

words = inquirer.fuzzy(
    message="Select preferred words:",
    choices=get_choices,
    multiselect=True,
    validate=lambda result: len(result) > 1,
    invalid_message="minimum 2 selections",
    max_height="70%",
).execute()

print(f'action: {action}, words: {words}')
