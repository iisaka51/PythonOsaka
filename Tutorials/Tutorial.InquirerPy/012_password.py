from InquirerPy import prompt
from InquirerPy.validator import PasswordValidator

original_password = "P@ssw0rd123"

questions = [
    {
        "type": "password",
        "message": "Old password:",
        "transformer": lambda _: "[hidden]",
        "validate": lambda text: text == original_password,
        "invalid_message": "Wrong password",
    },
    {
        "type": "password",
        "message": "New password:",
        "name": "new_password",
        "validate": PasswordValidator(
            length=8, cap=True, special=True, number=True
        ),
        "transformer": lambda _: "[hidden]",
    },
    {"type": "confirm", "message": "Confirm?", "default": True},
]

result = prompt(questions)
print(result)
