import code
import pickle
import sys

sys.ps1 = "pik> "
sys.ps2 = "...> "
banner = "Pik -- The stupid pickle loader.\nPress Ctrl-D to quit."

class PikConsole(code.InteractiveConsole):
    def runsource(self, source, filename="<stdin>"):
        if not source.endswith(pickle.STOP.decode()):
            return True  # more input is needed
        try:
            print(repr(pickle.loads(source.encode())))
        except:
            self.showsyntaxerror(filename)
        return False

pik = PikConsole()
pik.interact(banner)
