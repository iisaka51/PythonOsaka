import json
import pandas as pd

def readcsv(filename):
    df = pd.read_csv(filename)
    df.columns = df.columns.str.replace(' ', '_')
    return df

def write_json(df, filename):
    df.style.hide_index()
    df.to_json(filename)

if __name__ == '__main__':
    import typer

    def cli(csvfile: str = typer.Argument(...),
            dbfile: str = typer.Argument(...),
            debug: bool = typer.Option(False, "--debug")):
        if debug:
            print(f'csvfile: {csvfile}, dbfile: {dbfile}')
            raise typer.Exit()

        data = readcsv(csvfile)
        write_json(data, dbfile)

    typer.run(cli)
