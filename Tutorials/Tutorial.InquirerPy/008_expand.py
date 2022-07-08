from InquirerPy import prompt

fruits_choice = [
        {"key": "a", "name": "Apple", "value": "Apple"},
        {"key": "c", "name": "Cherry", "value": "Cherry"},
        {"key": "o", "name": "Orange", "value": "Orange"},
        {"key": "p", "name": "Peach", "value": "Peach"},
        {"key": "m", "name": "Melon", "value": "Melon"},
        {"key": "s", "name": "Strawberry", "value": "Strawberry"},
        {"key": "g", "name": "Grapes", "value": "Grapes"},
]

questions = [
    {
        "type": "expand",
        "choices": fruits_choice,
        "message": "Pick your favourite:",
        "default": "o",
        "cycle": False,
    },
]

result = prompt(questions)
print(result)
