import asyncio
import json
import logging

import websockets
from fastapi import HTTPException

from app.constants import (
    SECONDARIES_NODES,
    MESSAGE_REPLICATION_STATUS_OK,
    NUMBER_OF_MASTER_NODES,
)
from app.models.message import MessageOut

logger = logging.getLogger(__name__)


async def replicate_message(message: MessageOut, write_concern: int):
    tasks = []
    number_of_secondary_nodes_to_replicate = write_concern - NUMBER_OF_MASTER_NODES  # message already in master

    for i in range(number_of_secondary_nodes_to_replicate):
        tasks.append(send_to_secondary_nodes(SECONDARIES_NODES[i], message))

    for task in asyncio.as_completed(tasks):
        res = {}
        try:
            res = await task
            logger.info(res)
        except Exception as e:
            logger.error(e)
        finally:
            if res.get('acknowledgment') != MESSAGE_REPLICATION_STATUS_OK:
                logger.error(f"Failed to replicate message: {message}")
                raise HTTPException(status_code=500, detail=f"Failed replicate message: {message}.")


async def send_to_secondary_nodes(node: dict, msg: MessageOut) -> dict:
    logger.info(f"Connecting to {node['name']} ...")
    async with websockets.connect(node["url"]) as websocket:
        logger.info(f"Successfully connected to node: {node['name']}")
        await websocket.send(json.dumps(msg.dict()))
        acknowledgment = await websocket.recv()

        return {"node_name": node["name"], "acknowledgment": acknowledgment}
