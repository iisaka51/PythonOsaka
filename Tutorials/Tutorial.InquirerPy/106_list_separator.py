from InquirerPy import inquirer
from InquirerPy.separator import Separator

region = inquirer.select(
            message="Select regions:",
            choices=[
                {"name": "Sydney", "value": "ap-southeast-2"},
                {"name": "Singapore", "value": "ap-southeast-1"},
                Separator(),
                "us-east-1",
                Separator(line='*' * 15),
                "us-east-2",
            ],
            multiselect=True,
            transformer=lambda result: "%s region%s selected"
            % (len(result), "s" if len(result) > 1 else ""),
        ).execute()

print(region)
