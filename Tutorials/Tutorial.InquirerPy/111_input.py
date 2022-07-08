from prompt_toolkit.validation import Validator, ValidationError
from InquirerPy import inquirer

class AgeValidator(Validator):
    def validate(self, document):
        if int(document.text) < 18:
            raise ValidationError(
                message='Too yound.',
                cursor_position=len(document.text))  # Move cursor to end

first_name = inquirer.text(message="Waht's your first name?").execute()

default_name = 'Bauer' if first_name == 'Jack' else ''
last_name = inquirer.text(message="What's your last name?",
                        default=default_name).execute()
age = inquirer.text(message="How old are you?",
                        validate=AgeValidator()).execute()


print(f'first_name: {first_name}, last_name: {last_name}, age: {age}')
