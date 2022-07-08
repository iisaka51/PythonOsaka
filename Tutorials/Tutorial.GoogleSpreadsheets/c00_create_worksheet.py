import os
import gspread
from pathlib import Path

credential_dir = Path.home() / 'security'
keyfile = os.environ.get('PYTHONOSAKA_KEYFILE', default='credentials.json')
credential_path = credential_dir / keyfile
sheetname= 'PythonOsaka_tempsheet'

gc = gspread.service_account(filename=credential_path)

try:
    workbook = gc.open(sheetname)
except SpreadsheetNotFound:
    workbook = gc.create(sheetname)
    workbook.share('iisaka51@gmail.com', perm_type='user', role='owner')

worksheet = workbook.sheet1
