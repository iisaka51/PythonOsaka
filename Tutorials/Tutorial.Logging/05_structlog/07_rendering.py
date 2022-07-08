structlog.configure(processors=[structlog.processors.JSONRenderer()])
structlog.get_logger().msg("hi")
