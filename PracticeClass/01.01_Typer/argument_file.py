import typer

def cmd(srcfile: typer.FileText = typer.Argument(...)):
    lines = srcfile.readlines()
    for line in lines:
        typer.echo( line[:-1] )

if __name__ == '__main__':
    typer.run(cmd)
