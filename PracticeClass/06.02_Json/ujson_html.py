import ujson as json

html_data = "<script>Beer&Wine"
json_data = json.dumps(html_data, encode_html_chars=True)
print(json_data)
