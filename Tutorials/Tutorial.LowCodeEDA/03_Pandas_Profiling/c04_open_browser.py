import webbrowser
from pathlib import Path

html = Path('titanic.html')
url = 'file://' + str(html.absolute())
_ = webbrowser.open_new(url)
