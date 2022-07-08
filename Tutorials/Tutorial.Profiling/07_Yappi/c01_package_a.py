def a():
    for _ in range(10000000):
        pass


if __name__ == '__main__':
    import yappi

    yappi.set_clock_type("cpu")
    yappi.start()
    a()
    yappi.get_func_stats().print_all()
    yappi.get_thread_stats().print_all()
