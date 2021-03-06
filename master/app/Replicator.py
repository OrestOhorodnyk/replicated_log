import asyncio
import json
import logging

import websockets
from fastapi import HTTPException, BackgroundTasks

from app.constants import (
    SECONDARIES_NODES,
    MESSAGE_REPLICATION_STATUS_OK,
    NUMBER_OF_MASTER_NODES,
)
from app.models.message import MessageOut

logger = logging.getLogger(__name__)


async def replicate_to_minimum_required_nodes(message: MessageOut, write_concern: int):
    replication_number = write_concern - NUMBER_OF_MASTER_NODES  # message already in master

    tasks = [send_to_secondary_nodes(secondary, message) for secondary in SECONDARIES_NODES[:replication_number]]

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


def replicate_to_the_rest_of_nodes(message: MessageOut, write_concern: int, background_tasks: BackgroundTasks):
    replication_number = write_concern - NUMBER_OF_MASTER_NODES  # message already in master

    for secondary in SECONDARIES_NODES[replication_number:]:
        background_tasks.add_task(send_to_secondary_nodes, secondary, message)


async def send_to_secondary_nodes(node: dict, msg: MessageOut) -> dict:
    logger.info(f"Connecting to {node['name']} ...")
    async with websockets.connect(node["url"]) as websocket:
        logger.info(f"Successfully connected to node: {node['name']}")
        await websocket.send(json.dumps(msg.dict()))
        acknowledgment = await websocket.recv()

        return {"node_name": node["name"], "acknowledgment": acknowledgment}
