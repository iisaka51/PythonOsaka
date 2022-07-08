from aiohttp import ClientSession, TCPConnector
import asyncio
import pypeln as pl
from tqdm.asyncio import trange, tqdm
import time

limit = 1
users = list(range(1,10))

async def fetch(users, session):
    time.sleep(1)
    pbar.update(1)

with tqdm(total=len(users)) as pbar:
    pl.task.each(
        fetch,
        users,
        workers=limit,
        on_start=lambda: dict(session=ClientSession(connector=TCPConnector(limit=None,ssl=False))),
        on_done=lambda session: session.close(),
        run=True,
    )

