import os
import gspread
import pydantic
from pathlib import Path

class BaseSetting(pydantic.BaseSettings):
    class Config:
        env_prefix=''
        use_enum_values = True

class GSpreadConfig(BaseSetting):
    GSPREAD_CREDENTIAL_PATH: Path = Path.home() / 'security/credentials.json'
    GSPREAD_DEFAULT_USER: pydantic.EmailStr = '__YOUR_GMAIL_ADDRESS__@gmail.com'
    GSPREAD_PERM_TYPE: str = 'user'
    GSPREAD_ROLE: str = 'owner'

class GSpread(object):

    def __init__(self, filename='sample', sheetname='Sheet1', create=True):
        self.conf = GSpreadConfig()
        self.gc = gspread.service_account(
                     filename=self.conf.GSPREAD_CREDENTIAL_PATH)
        self.filename = filename
        self.sheetname = sheetname
        try:
            self.workbook = self.gc.open(self.filename)
        except gspread.SpreadsheetNotFound:
            self.workbook = self.gc.create(self.filename)
            self.workbook.share(
                self.conf.GSPREAD_DEFAULT_USER,
                perm_type=self.conf.GSPREAD_PERM_TYPE,
                role=self.conf.GSPREAD_ROLE)

        try:
            self.worksheet = self.workbook.worksheet(self.sheetname)
        except:
            if create:
                self.worksheet = self.workbook.add_worksheet(self.sheetname)
            else:
                self.worksheet = self.workbook.sheet1
                self.sheetname = self.worksheet.title

    @property
    def wb(self):
        return self.workbook

    @property
    def ws(self):
        return self.worksheet
