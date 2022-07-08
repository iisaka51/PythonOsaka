from InquirerPy import inquirer
from InquirerPy.validator import NumberValidator

answer = inquirer.text(
        message="What's your salary expectation(k):",
        transformer=lambda result: "%sk" % result,
        filter=lambda result: int(result) * 1000,
        validate=NumberValidator(),
).execute()

print(answer)
