def my_formatter(record, handler):
     return record.message

handler.formatter = my_formatter
