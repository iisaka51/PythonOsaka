from logbook import StderrHandler

handler = StderrHandler()
handler.format_string = '{record.channel}: {record.message}'
handler.formatter
