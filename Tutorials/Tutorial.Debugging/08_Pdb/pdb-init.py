def _pdb_init():
    import atexit
    import readline
    from pathlib import Path

    histfile = Path('~/.pdb-history').expanduser()
    if histfile.exists():
        readline.read_history_file(histfile)

    atexit.register(readline.write_history_file, histfile)
    readline.set_history_length(500)

_pdb_init()
del _pdb_init
