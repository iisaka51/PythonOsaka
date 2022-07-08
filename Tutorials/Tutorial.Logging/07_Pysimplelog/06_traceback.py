from mylogger import logger

# トレースバックをロギング
import traceback
try:
    1/range(10)
except Exception as err:
    logger.error(f'{err} (is this python ?)',
                 tback=traceback.extract_stack())
