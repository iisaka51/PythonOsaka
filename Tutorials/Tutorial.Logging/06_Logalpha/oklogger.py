import sys
from dataclasses import dataclass
from typing import List, IO, Callable

from logalpha.color import Color, ANSI_RESET
from logalpha.level import Level
from logalpha.message import Message
from logalpha.handler import StreamHandler
from logalpha.logger import Logger

class OkayLogger(Logger):
    """Logger with Ok/Err levels."""

    levels: List[Level] = Level.from_names(['Ok', 'Err'])
    colors: List[Color] = Color.from_names(['green', 'red'])

@dataclass
class OkayHandler(StreamHandler):
    """
    Writes to <stderr> by default.
    Message format includes the colorized level and the text.
    """

    level: Level = OkayLogger.levels[0]  # Ok
    resource: IO = sys.stderr

    def format(self, message: Message) -> str:
        """Format the message."""
        color = OkayLogger.colors[message.level.value].foreground
        return f'{color}{message.level.name:<3}{ANSI_RESET} {message.content}'
