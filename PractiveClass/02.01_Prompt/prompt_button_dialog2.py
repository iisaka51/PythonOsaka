from prompt_toolkit.shortcuts import button_dialog

def main():
    result = button_dialog(
        title="Button dialog example",
        text="Which do you like?",
        buttons=[
           ("Box1", 1), ("Box2", 2), ("Box3", 3),
           ("Box4", 4), ("Box5", 5), ("Box6", 6),
           ("Box7", 7), ("Box8", 8), ("Box9", 9),
        ],
    ).run()

    print("Result = {}".format(result))

if __name__ == "__main__":
    main()
