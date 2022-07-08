from InquirerPy import inquirer

first_name = inquirer.text(
                      message="What's your first name: ").execute()
if first_name != '':
    last_name = inquirer.text(
                          message="What's your last name: ").execute()
else:
    last_name = ''

print(first_name, last_name)
