from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator

original_password = "P@ssw0rd123"

old_password = inquirer.secret(
    message="Old password:",
    transformer=lambda _: "[hidden]",
    validate=lambda text: text == original_password,
    invalid_message="Wrong password",
).execute()

new_password = inquirer.secret(
    message="New password:",
    validate=PasswordValidator(length=8, cap=True, special=True, number=True),
    transformer=lambda _: "[hidden]",
).execute()

confirm = inquirer.confirm(message="Confirm?", default=True).execute()

msg = f'old_password: {old_password}, '
msg += f'new_password: {new_password}, '
msg += f'confirm: {confirm}'
print(f'{msg}')
