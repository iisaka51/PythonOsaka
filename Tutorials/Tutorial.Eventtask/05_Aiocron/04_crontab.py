import aiocron
import asyncio
from datetime import datetime

async def attime():
    print(f'{datetime.now()}')

cron = aiocron.crontab('*/2 * * * *', func=attime, start=False)
loop = asyncio.get_event_loop()

try:
    cron.start()
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
