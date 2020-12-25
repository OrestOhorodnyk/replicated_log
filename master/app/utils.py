import asyncio
import logging
import sys
from app.constants import MAX_DELAY_BEFORE_RETRY_SECONDS

logger = logging.getLogger(__name__)


def retry(times):
    def func_wrapper(f):
        async def wrapper(*args, **kwargs):
            for time in range(times):
                error = None
                delay = time + 1
                await asyncio.sleep(delay if delay < MAX_DELAY_BEFORE_RETRY_SECONDS else MAX_DELAY_BEFORE_RETRY_SECONDS)
                try:
                    return await f(*args, **kwargs)
                except Exception as exc:
                    error = exc
                    pass
                logger.info(f"Retrying {f.__name__} ... Attempt # {time + 1}. Args {args}")
            raise error

        return wrapper

    return func_wrapper


def id_generator():
    for i in range(1, sys.maxsize):
        yield i


ID_GENERATOR = id_generator()
