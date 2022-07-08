import sys
import io
from typing import Type, List, IO, Callable
from dataclasses import dataclass
from datetime import datetime
from socket import gethostname

from logalpha.color import Color, ANSI_RESET
from logalpha.handler import StreamHandler
from logalpha.level import Level
from logalpha.message import Message
from logalpha.logger import Logger

HOST: str = gethostname()

@dataclass
class DetailedMessage(Message):
    """A message with additional attributes."""
    level: Level
    content: str
    timestamp: datetime
    topic: str
    host: str

class DetailedLogger(Logger):
    """Logger with detailed messages."""

    Message: Type[Message] = DetailedMessage
    topic: str

    def __init__(self, topic: str) -> None:
        """Initialize with `topic`."""
        super().__init__()
        self.topic = topic
        self.callbacks = {'timestamp': datetime.now,
                          'host': (lambda: HOST),
                          'topic': (lambda: topic)}
