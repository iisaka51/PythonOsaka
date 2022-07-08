from InquirerPy import prompt

questions = [
    {
        'type': 'input',
        'name': 'first_name',
        'message': "What's your first name",
    },
    {
        'type': 'input',
        'name': 'last_name',
        'message': "What's your last name",
        'when': lambda answers: answers['first_name'] != '',
    }
]

answers = prompt(questions)
print(answers)
