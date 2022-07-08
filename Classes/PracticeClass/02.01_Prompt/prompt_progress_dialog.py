import os
import time

from prompt_toolkit.shortcuts import progress_dialog

def worker(set_percentage, log_text):
    """
    この関数は`progress_dialog` から呼び出され、
    バックグランドで実行されます。
    """
    percentage = 0
    for dirpath, dirnames, filenames in os.walk("/tmp"):
        for f in filenames:
            log_text("{} / {}\n".format(dirpath, f))
            set_percentage(percentage + 1)
            percentage += 2
            time.sleep(0.1)

            if percentage == 100:
                break
        if percentage == 100:
            break

    set_percentage(100)
    time.sleep(120)


def main():
    progress_dialog(
        title="Progress dialog example",
        text="As an examples, we walk through the filesystem and print "
        "all directories",
        run_callback=worker,
    ).run()

if __name__ == "__main__":
    main()
