from logbook import warning, StreamHandler
import sys
StreamHandler(sys.stdout).push_application()
warning('This is a warning')
