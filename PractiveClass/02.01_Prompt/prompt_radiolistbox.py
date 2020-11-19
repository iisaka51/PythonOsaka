from prompt_toolkit.shortcuts import radiolist_dialog

def main():
    result = radiolist_dialog(
        values=[
            ("red", "Red"),
            ("green", "Green"),
            ("blue", "Blue"),
            ("orange", "Orange"),
        ],
        title="Radiolist dialog example",
        text="Please select a color:",
    ).run()

    print("Result = {}".format(result))


if __name__ == "__main__":
    main()
