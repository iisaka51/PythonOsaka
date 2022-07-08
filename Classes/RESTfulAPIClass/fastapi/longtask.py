from fastapi import FastAPI, BackgroundTasks
from time import sleep
from datetime import datetime

app = FastAPI()

def slow_task(count: int):
    sleep(count)
    print(f'done. {datetime.utcnow()}')

@app.get('/{count}')
def back(count: int, background_tasks: BackgroundTasks):
    """ example for background jobs """
    background_tasks.add_task(slow_task, count)
    return {"result": f"finish {datetime.utcnow()}"}
