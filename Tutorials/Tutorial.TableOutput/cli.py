import typer
from prettytable import PrettyTable, from_csv, from_md


def from_md(md, **kwargs):
    """
    Generate PrettyTable from markdown string.
    :param md: markdown type string.
    :return: a PrettyTable object.
    """
    rows = md.split('\n')
    title_row = rows[0]
    content_rows = rows[2:]
    table = PrettyTable(**kwargs)
    table.field_names = split_md_row(title_row)
    map(table.add_row, map(split_md_row,
                           filter(lambda x: x, content_rows)))
    return table

def strip_md_content(s):
    """
    Strip the blank space and `:` in markdown table content cell.
    :param s: a row of markdown table
    :return: stripped content cell
    """
    return s.strip().strip(':').strip()

def split_md_row(row):
    """
    Split markdown table.
    :param row: a row of markdown table
    :return: Split content list
    """
    return [strip_md_content(s) for s in row.strip('|').split('|')]



def main(csv: bool = typer.Option(False, "--csv",
                                  help='Parse as CSV format'),
         json: bool = typer.Opton(False, "--json",
                                  help='Parse as JSON format'),
         markdown: bool = typer.Opton(False, "--md", "--markdown",
                                  help='Parse as Markdown format'),
         rst: bool = typer.Opton(False, "--rst",
                                  help='ParsParse as reStructuredText format'),
         args: List[str] = typer.Arguments(..., help="file path")
):
    if csv:
        with open(args.csv) as fp:
            print(from_csv(fp))
    elif md:
        with open(args.md) as md:
            print(from_md(md.read()))
    else:
        text_in = sys.stdin.read()
        print(from_csv(StringIO.StringIO(text_in)))


if __name__ == '__main__':
    app()
