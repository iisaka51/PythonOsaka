import structlog

class CustomPrintLogger:
    def msg(self, message):
        print(message)

def proc(logger, method_name, event_dict):
    print("I got called with", event_dict)
    return repr(event_dict)

log = structlog.wrap_logger(
    CustomPrintLogger(),
    wrapper_class=structlog.BoundLogger,
    processors=[proc],
)

# log2 = log.bind(x=42)
# log == log2
# log.msg("hello world")
# log2.msg("hello world")

# log3 = log2.unbind("x")
# log == log3
# log3.msg("nothing bound anymore", foo="Python")
