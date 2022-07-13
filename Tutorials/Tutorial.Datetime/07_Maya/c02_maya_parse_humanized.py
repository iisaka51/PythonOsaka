import maya

tests = [
    "22th of february 2022",
    "2/22/2022",
    "2-22-2022",
    "2 22 2022",
    "Feb 22 2022",
    "February 22 2022",
    "February 22st 2022",
    "22st of february 2022",
    "2022年2月22日",
]

for str_date in tests:
    try:
        d = maya.parse(str_date).datetime()
        print(d)
    except Exception as msg:
        print(f'Raise Exception: {msg}')
