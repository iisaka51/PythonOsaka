from prompt_toolkit.shortcuts import yes_no_dialog

def main():
    result = yes_no_dialog(
        title="Beer Select dialog",
        text="Which do you Like?",
        yes_text="IPA",
        no_text="LAGER"
    ).run()

    print("Result = {}".format(result))

if __name__ == "__main__":
    main()
