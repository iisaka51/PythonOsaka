import timeout

@timeout.timeout(duration=0.5)
def foo(value: int) -> None:
    # ...
    pass


@timeout.timeout(duration=0.5)
def bar(self, value: str) -> str:
    # ...
    pass

