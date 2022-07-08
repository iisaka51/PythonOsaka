from structlog import get_logger

logger = get_logger()
def some_function(data: str = 'python') -> str:
    logger.error("previous data", name=data)
    return data.upper()
