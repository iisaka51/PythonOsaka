import aiocron
import asyncio
from datetime import datetime

@aiocron.crontab('*/2 * * * *')
async def attime():
    print(f'{datetime.now()}')

loop = asyncio.get_event_loop()

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
