import structlog

def proc(logger, method_name, event_dict):
    print("I got called with", event_dict)
    return repr(event_dict)

structlog.configure(processors=[proc], context_class=dict)
log = structlog.wrap_logger(structlog.PrintLogger())
log.msg("hello world")
