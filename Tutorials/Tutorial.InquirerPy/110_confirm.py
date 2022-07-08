from InquirerPy import inquirer

proceed, service, confirm = False, False, False
proceed = inquirer.confirm(message="Proceed?", default=True).execute()
if proceed:
    service = inquirer.confirm(message="Require 1 on 1?").execute()
if service:
    confirm = inquirer.confirm(message="Confirm?").execute()

print(f'proceed:{proceed}, service:{service}, confirm:{confirm}')
