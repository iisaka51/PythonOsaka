from gspread_utils import GSpread

US_constitution = """\
We the People of the United States, in Order to form a more perfect Union, establish Justice, insure domestic Tranquility, provide for the common defense, promote the general Welfare, and secure the Blessings of Liberty to ourselves and our Posterity, do ordain and establish this Constitution for the United States of America."""

ws = GSpread("PythonOsaka_tempfile").worksheet


_ = ws.clear()
_ = ws.update('A1', [[ US_constitution ]])

formula = f'=GoogleTranslate(A1, "en", "ja")'
_ = ws.update('B1', formula, raw=False)

v1 = ws.acell('B1').value
