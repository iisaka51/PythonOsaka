from InquirerPy import inquirer
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

regions = inquirer.checkbox(
    message="Select regions:",
    choices=region_choice,
    cycle=False,
    transformer=lambda result: "%s region%s selected"
    % (len(result), "s" if len(result) > 1 else ""),
).execute()
print(regions)
