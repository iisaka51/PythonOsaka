def task_cleanup():
    """ Cleanup test files """
    return {
        "actions": [
            "rm -f cat-in.txt cat-out.txt hello*.txt all.txt random-*txt"
        ]
    }

def task_clearn_runinfo():
    """ Cleanup runinfo """
    return {
        "actions": [
            "rm -rf runinfo"
        ]
    }
