from InquirerPy import prompt

questions = [
    {
        'type': 'input',
        'name': 'first_name',
        'message': "What's your first name",
    }
]

answers = prompt(questions)
print(answers)
print(answers['first_name'])
