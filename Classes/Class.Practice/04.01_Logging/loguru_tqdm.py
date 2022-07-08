import time

from loguru import logger
from tqdm import tqdm

logger.remove()
logger.add(tqdm.write)

logger.info("Initializing")

for x in tqdm(range(100)):
    logger.info("Iterating #{}", x)
    time.sleep(1)
