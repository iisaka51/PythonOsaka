loop = asyncio.get_event_loop()
now = loop.time()

async with timeout_at(now + 1.5):
    await inner()
