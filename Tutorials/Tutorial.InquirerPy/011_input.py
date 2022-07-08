from prompt_toolkit.validation import Validator, ValidationError
from pprint import pprint
from InquirerPy import prompt

class AgeValidator(Validator):
    def validate(self, document):
        if int(document.text) < 18:
            raise ValidationError(
                message='Too yound.',
                cursor_position=len(document.text))  # Move cursor to end

questions = [
  {
    'type': 'input',
    'name': 'first_name',
    'message': "What's your first name ?",
  },
  {
    'type': 'input',
    'name': 'last_name',
    'message': "What's your last name ?",
    'default': lambda ans: 'Bauer' if ans['first_name'] == 'Jack' else '',
  },
  {
    'type': 'input',
    'name': 'age',
    'message': "How old are you ?",
    'validate': AgeValidator()
  }
]
result = prompt(questions)
pprint(result)
