import json
import logging

import websockets
from fastapi import HTTPException

from app.constants import SECONDARIES_NODES, MESSAGE_REPLICATION_STATUS_OK
from app.models.message import MessageOut

logger = logging.getLogger(__name__)


async def replicate_message(message: MessageOut):
    for node in SECONDARIES_NODES:
        acknowledgment = None
        try:
            acknowledgment = await send_to_secondary_nodes(node["url"], message)
        except Exception as e:
            logger.error(e)
        finally:
            if acknowledgment != MESSAGE_REPLICATION_STATUS_OK:
                logger.error(f"Failed to replicate message to {node['name']}, message {message}")
                raise HTTPException(status_code=500, detail=f"Failed replicate message {message} to {node['name']}.")


async def send_to_secondary_nodes(uri: str, msg: MessageOut) -> str:
    async with websockets.connect(uri) as websocket:
        logger.info("Connected..")
        await websocket.send(json.dumps(msg.dict()))
        acknowledgment = await websocket.recv()
        return acknowledgment
