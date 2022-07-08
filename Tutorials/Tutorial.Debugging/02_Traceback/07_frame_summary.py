def my_divide(a, b):
    return a / b

if __name__ == '__main__':
    import sys
    from traceback import StackSummary, walk_stack
    template = (
        '{frame.filename}:{frame.lineno}:{frame.name}:\n'
        '    {frame.line}'
    )
    data = [1,0,2,3]
    for n in data:
        try:
            print(my_divide(1,n))
        except ZeroDivisionError:
            summary = StackSummary.extract(walk_stack(None))
            for frame in summary:
                print(template.format(frame=frame))
    print('done.')
