import asyncio
from constants import MAX_DELAY_BEFORE_RETRY_SECONDS
import logging

logger = logging.getLogger(__name__)


def retry(times):
    def func_wrapper(f):
        async def wrapper(*args, **kwargs):
            for time in range(times):
                delay = time+1
                await asyncio.sleep(delay if delay <zl MAX_DELAY_BEFORE_RETRY_SECONDS else MAX_DELAY_BEFORE_RETRY_SECONDS)
                try:
                    return await f(*args, **kwargs)
                except Exception as exc:
                    pass
            raise

        return wrapper

    return func_wrapper
