import asyncio
import json
import logging

from fastapi import APIRouter

from app.constants import MESSAGE_REPLICATION_STATUS_OK
from app.message_model import Message
from app.msg_manager import MsgManager

router = APIRouter()
msg_manager = MsgManager()
logger = logging.getLogger(__name__)


@router.get("/status")
async def status():
    return {"status": "OK"}


@router.get("/list_msg")
async def list_msg():
    return msg_manager.get_messages()


@router.websocket_route("/append_msg")
async def append_msg(websocket):
    logger.info("WEBSOKET ACCEPT CONNECTION")
    await websocket.accept()
    msg_txt = await websocket.receive_text()
    msg_json = json.loads(msg_txt)
    message = Message(**msg_json)
    msg_manager.add_msg(message)
    await asyncio.sleep(5)
    await websocket.send_text(MESSAGE_REPLICATION_STATUS_OK)
    await websocket.close()
    logger.info("WEBSOKET CLOSED")
