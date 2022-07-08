from prompt_toolkit import prompt

password = prompt('Enter password: ', is_password=True)
print(f'Your password: {password}')
