from InquirerPy import inquirer

fruit = inquirer.rawlist(
    message="Pick your favourites:",
    choices=[
        "Apple",
        "Orange",
        "Peach",
        "Cherry",
        "Melon",
        "Strawberry",
        "Grapes",
    ],
    default=3,
    multiselect=True,
    transformer=lambda result: ", ".join(result),
    validate=lambda result: len(result) > 1,
    invalid_message="Minimum 2 selections",
).execute()

print(fruit)
