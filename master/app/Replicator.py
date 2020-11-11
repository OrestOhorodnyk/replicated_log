import requests

from app.constants import SECONDARIES_NODES
from app.models.message import Message


async def replicate_message(message: Message):
    for url in SECONDARIES_NODES:
        response = requests.post(url, json=message.to_dict())
        print(response.status_code)
