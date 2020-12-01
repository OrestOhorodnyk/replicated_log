import asyncio
import json
import logging
from typing import List

from fastapi import APIRouter
from app.constants import DELAY
from app.constants import MESSAGE_REPLICATION_STATUS_OK
from app.models.message import Message
from app.msg_list import MsgList

router = APIRouter()
msg_list = MsgList()
logger = logging.getLogger(__name__)


@router.get("/status")
async def status():
    return {"status": "OK"}


@router.get("/list_msg", status_code=200, response_model=List[Message])
async def list_msg():
    return msg_list.get_messages()


@router.websocket_route("/append_msg")
async def append_msg(websocket):
    logger.info("WEBSOKET ACCEPT CONNECTION")
    await websocket.accept()
    msg_txt = await websocket.receive_text()
    msg_json = json.loads(msg_txt)
    message = Message(**msg_json)
    await asyncio.sleep(DELAY)
    msg_list.add_msg(message)
    await websocket.send_text(MESSAGE_REPLICATION_STATUS_OK)
    await websocket.close()
    logger.info("WEBSOKET CLOSED")
