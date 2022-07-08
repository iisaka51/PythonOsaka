import aiocron
import asyncio

# @aiocron.crontab('0 9,10 * sun,mon', start=False)
@aiocron.crontab('* * * * sun,mon', start=False)
async def attime(i):
    print('run %i' % i)

async def once():
    try:
        res = await attime.next(1)
    except Exception as e:
        print('It failed (%r)' % e)
    else:
        print(res)

loop = asyncio.get_event_loop()
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
