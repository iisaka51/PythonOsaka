from beautifultable import BeautifulTable

table = BeautifulTable(maxwidth=40)
table.columns.header = ["Heading 1", "Heading 2"]
table.rows.append(["first Line\nsecond Line", "single line"])
table.rows.append(["first Line\nsecond Line\nthird Line",
                   "first Line\nsecond Line"])
table.rows.append(["UTF8エンコーディングをサポートしています",
                   "日本語の表示と折返しもOKです"])

print(table)
