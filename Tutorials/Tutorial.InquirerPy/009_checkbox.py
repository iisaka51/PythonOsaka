from InquirerPy import prompt
from InquirerPy.separator import Separator

region_choice = [
    Separator(),
    {"name": "Sydney", "value": "ap-southeast-2", "enabled": False},
    {"name": "Singapore", "value": "ap-southeast-1", "enabled": True},
    Separator(),
    "us-east-1",
    "us-west-1",
    Separator(),
]

questions = [
    {
        "type": "checkbox",
        "message": "Select regions:",
        "choices": region_choice,
        "transformer": lambda result: "%s region%s selected"
        % (len(result), "s" if len(result) > 1 else ""),
    },
]

result = prompt(questions)
print(result)
