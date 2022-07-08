import aiocron
import asyncio
from datetime import datetime

@aiocron.crontab('1 9 * * *', start=False)
async def attime():
    print(f'{datetime.now()}')

loop = asyncio.get_event_loop()
try:
    attime.start()
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
