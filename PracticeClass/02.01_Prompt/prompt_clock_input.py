import datetime
from prompt_toolkit.shortcuts import prompt

def get_prompt():
    now = datetime.datetime.now()
    return [
        ("bg:#008800 #ffffff", "%s:%s:%s" % (now.hour, now.minute, now.second)),
        ("bg:cornsilk fg:maroon", " Enter something: "),
    ]

def main():
    result = prompt(get_prompt, refresh_interval=0.5)
    print("You said: %s" % result)

if __name__ == "__main__":
    main()