import logging

import requests
from requests.exceptions import ConnectionError
from app.constants import SECONDARIES_NODES
from app.models.message import MessageOut

logger = logging.getLogger(__name__)


async def replicate_message(message: MessageOut):
    for url in SECONDARIES_NODES:
        try:
            response = requests.post(url, json=message.dict())
            logger.info(f'message replicated to : "{url}", status: {response.status_code}')
        except ConnectionError as e:
            logger.error(f'failed to replicate message: "{message.dict()}" to {url}, error: {e}')
