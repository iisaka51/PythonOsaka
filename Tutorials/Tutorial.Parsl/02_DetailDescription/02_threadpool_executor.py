import parsl
from parsl.app.app import python_app

conf = parsl.load()

answer = 42

@python_app
def print_answer():
    print('the answer is', answer)

app = print_answer()
app.result()
