from prompt_toolkit import prompt
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.key_binding import KeyBindings

bindings = KeyBindings()

@bindings.add('c-x')
def _(event):
    " Exit when `c-x` is pressed. "
    event.app.exit()

def status_line():
    return 'To exit Ctl+x.'

while True:
    user_input = prompt(' >>>> ',
                        bottom_toolbar=status_line,
                        key_bindings=bindings,
                        )
    print(user_input)
