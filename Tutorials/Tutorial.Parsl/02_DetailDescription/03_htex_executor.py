import parsl
from parsl.app.app import python_app
from htex_config import htex_config

parsl.clear()
conf = parsl.load(htex_config)

answer = 42

@python_app
def print_answer():
    print('the answer is', answer)

app = print_answer()
app.result()
