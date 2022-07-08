from InquirerPy import inquirer

name = inquirer.text(message="What's your name: ").execute()
print(name)
