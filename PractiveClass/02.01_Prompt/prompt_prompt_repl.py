from prompt_toolkit import prompt

def status_line():
    return 'To exit Ctl+C or Ctl+D.'


while True:
    user_input = prompt(' >>>> ',
                        bottom_toolbar=status_line,
                        )
    print(user_input)
