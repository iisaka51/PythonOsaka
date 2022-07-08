from InquirerPy import inquirer
from InquirerPy.separator import Separator

action = inquirer.select(
        message="Select an action:",
        choices=["Upload", "Download", {"name": "Exit", "value": None}],
        default=None,
        # multiselect=True,
).execute()

print(action)
