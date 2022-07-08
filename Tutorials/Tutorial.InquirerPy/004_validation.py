from InquirerPy import prompt
from InquirerPy.validator import NumberValidator

questions = [
   {
       "name": "request salary",
       "type": "input",
       "message": "What's your salary expectation(k):",
       "transformer": lambda result: "%sk" % result,
       "filter": lambda result: int(result) * 1000,
       "validate": NumberValidator(),
   },
]

answer = prompt(questions)
print(answer)
