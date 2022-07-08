def greeing(name, message, caps):
    output = f'{greeting} {name}'
    if caps:
        output = output.upper()
    return output

