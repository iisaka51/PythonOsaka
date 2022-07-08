# Automate Googlesheet
# pip install gspread
# Note: You can easily get crediential file from googlesheet

import gspread
ws = gspread.service_account('test_crediential.json')

# Open sheet with Url or Name
sheet = ws.open("Medium Table")
sheet = ws.open_by_url("https://docs.google.com/full_url")

# Get First Sheet
sheet = sheet.sheet1

# Get all Data from Sheet
sheet_data = sheet.get_all_values()

# Get Specific Row
sheet_data = sheet.row_values(1)

# Get Specific Column
sheet_data = sheet.col_values(1)

# Get Specific Cell
sheet_data = sheet.cell(1, 1).value

# Finding Cell with match String
sheet_data = sheet.find("string").row

# Update data in Sheet
sheet.update("A1", "Medium Article")

# Update data with row and column
sheet.update_cell(1, 1, "Medium Article")

# Append data to Sheet
sheet.append_row(["Medium Article12"])

# Delete data from row
sheet.delete_row(1)

# Data data from col
sheet.delete_col(1)

# Delete data from cell
sheet.delete_cell(1, 1)

# Format the Row and Col
sheet.format('A1:B2', {'textFormat': {'bold': True}})

# Format Color of Row and Col
sheet.format('A1:B2', {'backgroundColor': {'red': 1.0}})

# Format Font Size of Row and Col
sheet.format('A1:B2', {'textFormat': {'fontSize': 12}})

# Format Font Family of Row and Col
sheet.format('A1:B2', {'textFormat': {'fontFamily': 'Arial'}})
