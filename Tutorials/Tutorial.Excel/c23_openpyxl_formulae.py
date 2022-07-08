from openpyxl import Workbook
from openpyxl.utils import FORMULAE
from openpyxl.formula import Tokenizer

formula = """=IF($A$1,"then True",MAX(DEFAULT_VAL,'Sheet 2'!B1))"""
tok = Tokenizer(formula)

print("\n".join("%12s%11s%9s" % (t.value, t.type, t.subtype) for t in tok.items))

# FORMULAE


