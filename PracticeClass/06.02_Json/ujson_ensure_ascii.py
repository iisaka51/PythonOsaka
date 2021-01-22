import ujson as json

data = "åäö"
ascii_data = json.dumps(data, encode_html_chars=True)
print(ascii_data)
