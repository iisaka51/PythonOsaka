from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

_ = ws.batch_clear(["F1:H2"])

# ワークシート全体をクリアするときは
# _ = ws.clear()

