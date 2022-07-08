from InquirerPy import inquirer

fruits_choice = [
        {"key": "a", "name": "Apple", "value": "Apple"},
        {"key": "c", "name": "Cherry", "value": "Cherry"},
        {"key": "o", "name": "Orange", "value": "Orange"},
        {"key": "p", "name": "Peach", "value": "Peach"},
        {"key": "m", "name": "Melon", "value": "Melon"},
        {"key": "s", "name": "Strawberry", "value": "Strawberry"},
        {"key": "g", "name": "Grapes", "value": "Grapes"},
    ]

fruit = inquirer.expand(
        message="Pick your favourite:",
        choices=fruits_choice,
        default="o"
    ).execute()

print(fruit)
