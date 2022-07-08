#from functools import lru_cache
from typing import Iterator
from sqlalchemy.orm import Session
from fastapi_utils.session import FastAPISessionMaker

def get_db() ->Iterator[Session]:
    yield from _get_fastapi_sessionmaker().get_db()


#@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    database_uri = 'sqlite:///todo.db'
    return FastAPISessionMaker(database_uri)

