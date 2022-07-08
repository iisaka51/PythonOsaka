from InquirerPy import prompt

questions = [
    {
        "type": "rawlist",
        "choices": [
            "Apple", "Orange", "Peach", "Cherry",
            "Melon", "Strawberry", "Grapes",
        ],
        "message": "Pick your favourites:",
        "default": 3,
        "multiselect": True,
        "transformer": lambda result: ", ".join(result),
        "validate": lambda result: len(result) > 1,
        "invalid_message": "Minimum 2 selections",
    },
]

fruits = prompt(questions)
print(fruits)
