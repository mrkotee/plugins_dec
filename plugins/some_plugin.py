
from database.models import User
from loguru import logger


print("first plug")


def before():
    # print("before")
    u = User()
    print(f"user model: {u}")

    logger.debug("log before")


def some_unsused_func():
    print("not used print")

1/0
