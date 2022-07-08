import os

class MyLogger(logbook.Logger):

    def process_record(self, record):
        logbook.Logger.process_record(self, record)
        record.extra['cwd'] = os.getcwd()
