from pygments.lexers.html import HtmlLexer
from pygments.styles import get_style_by_name
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls

style = style_from_pygments_cls(get_style_by_name('monokai'))
text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer), style=style,
              include_default_pygments_style=False)
print('You said: %s' % text)
