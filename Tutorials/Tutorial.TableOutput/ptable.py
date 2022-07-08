import typer
from prettytable import PrettyTable

app = typer.Typer()

@app.command()
main(csv: ZZ
     filename: typer.FileText = typer.Argument(...)):

