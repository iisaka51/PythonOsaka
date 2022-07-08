def main(dsn, command: ("SQL query", 'option')="select * from table"):
    if command:
        print('executing %s on %s' % (command, dsn))
        # ...

if __name__ == '__main__':
    import plac
    plac.call(main)
