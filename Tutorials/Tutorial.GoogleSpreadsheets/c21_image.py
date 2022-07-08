from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート1").worksheet
_ = ws.clear()

image_url='https://www.google.com/images/srpr/logo3w.png'

A_cells = ws.range("A1:A5")
for n, cell in enumerate(A_cells):
    cell.value = f'=Image(B{n+1})'

B_cells = ws.range("B1:B5")
for cell in B_cells:
    cell.value = image_url

_ = ws.update_cells(B_cells)
_ = ws.update_cells(A_cells, value_input_option="USER_ENTERED")
