from InquirerPy import prompt

questions = [
   {
       "type": "input",
       "message": "Which company would you like to apply:",
       "completer": {
           "Google": None,
           "Facebook": None,
           "Amazon": None,
           "Netflix": None,
           "Apple": None,
           "Microsoft": None,
       },
       "multicolumn_complete": True,
   },
]

answers = prompt(questions)
print(answers)
