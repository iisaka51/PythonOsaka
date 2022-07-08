from InquirerPy import inquirer

answer = inquirer.text(
        message="Which company would you like to apply:",
        completer={
            "Google": None,
            "Facebook": None,
            "Amazon": None,
            "Netflix": None,
            "Apple": None,
            "Microsoft": None,
        },
        multicolumn_complete=True,
    ).execute()

print(answer)
