
from loguru import logger


print("second plug")


def after():
    print('plg after')
    logger.debug("some after log")
