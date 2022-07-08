import sqlite3
import pandas as pd

def readcsv(filename):
    df = pd.read_csv(filename)
    df.columns = df.columns.str.replace(' ', '_')
    return df

def writedb(df, filename):
    conn = sqlite3.connect(filename)
    table_name = filename.split('.')[0]
    df.to_sql(table_name, conn, if_exists='replace')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    import typer

    def cli(csvfile: str = typer.Argument(...),
            dbfile: str = typer.Argument(...),
            debug: bool = typer.Option(False, "--debug")):
        if debug:
            print(f'csvfile: {csvfile}, dbfile: {dbfile}')
            raise typer.Exit()

        data = readcsv(csvfile)
        writedb(data, dbfile)

    typer.run(cli)
