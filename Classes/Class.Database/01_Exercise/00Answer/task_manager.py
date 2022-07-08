import click
from click_shell import shell
# from tinydb_task import *
from zodb_task import *

db = TaskDB()

@shell(prompt='task> ', intro='Starting task manager...')
def app():
    pass

@app.command()
@click.argument('title', nargs=1)
@click.argument('description', nargs=1)
def add(title, description):
    task_id = db.add(title, description)
    click.echo(f'id: {task_id} added')

@app.command()
@click.argument('task_id', type=int, nargs=1)
@click.argument('title', nargs=1)
@click.argument('description', nargs=1)
def update(task_id, task):
    task_id = db.update(title, decription, task_id)
    click.echo(f'id: {task_id} updated')

@app.command()
@click.argument('task_id', type=int, nargs=1)
def remove(task_id):
    db.remove(task_id)
    click.echo(f'id: {task_id} removed')

@app.command()
@click.argument('task_id', type=int, nargs=1)
def get(task_id):
    task = db.get(task_id)
    click.echo(f'id: {task_id} {task}')

@app.command()
@click.argument('task_id', type=int, nargs=1)
def done(task_id):
    task_id = db.update(task_id)
    click.echo(f'id: {task_id} set done flag.')

@app.command()
def listall():
    print(db.tasks)
    for task_id, task in enumerate(db.list()):
        click.echo(f'id: {task_id} {task}')

if __name__ == '__main__':
    app()
