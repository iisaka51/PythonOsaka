from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme

class EmailHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""

    base_style = "example."
    highlights = [r"(?P<email>[\w-]+@([\w-]+\.)+[\w-]+)"]


theme = Theme({"example.email": "bold magenta"})
highlight_emails = EmailHighlighter()

console = Console(highlighter=highlight_emails, theme=theme)
console.print("Send funds to money@example.org")

console.print(highlight_emails("Send funds to money@example.org"))
