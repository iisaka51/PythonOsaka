import inspect

def my_function():
    frame = inspect.currentframe()
    return inspect.getframeinfo(frame)

f = my_function()

print(f'filename={f.filename}')
print(f'lineno={f.lineno}')
print(f'function={f.function}')
print(f'code_context={f.code_context}')
print(f'index={f.index}')
