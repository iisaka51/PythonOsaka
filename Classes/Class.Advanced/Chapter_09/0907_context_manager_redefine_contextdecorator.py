from contextlib import ContextDecorator

class makeHtml(ContextDecorator):
    def __enter__(self):
        print('<html>')
        print('<body>')
        print('<p>')
        return self

    def __exit__(self, *exc):
        print('</p>')
        print('</body>')
        print('</html>')
        return False

@makeHtml()
def gen_html():
    print('Here is simple text.')

gen_html()
