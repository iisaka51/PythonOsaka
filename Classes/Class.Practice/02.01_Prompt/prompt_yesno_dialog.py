from prompt_toolkit.shortcuts import yes_no_dialog

def main():
    result = yes_no_dialog(
        title="Yes/No dialog example",
        text="どっちがええねん?"
        # text="Do you want to confirm?"
    ).run()

    print("Result = {}".format(result))

if __name__ == "__main__":
    main()
