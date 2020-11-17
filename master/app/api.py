import logging
from datetime import datetime

from fastapi import APIRouter

from app.Replicator import replicate_message
from app.models.message import MessageOut, MessageIn
from app.msg_list import MsgList

router = APIRouter()
msg_list = MsgList()
logger = logging.getLogger(__name__)


@router.get("/status")
async def status():
    return {"status": "OK"}


@router.get("/list_msg")
async def list_msg():
    return msg_list.get_messages()


@router.get("/list_size")
async def list_size():
    return {"list size": len(msg_list.get_messages())}


@router.post("/append_msg", status_code=201, response_model=MessageOut)
async def append_msg(msg: MessageIn):
    message = MessageOut(message=msg.message, created_at=str(datetime.utcnow()))
    msg_list.add_msg(message)
    await replicate_message(message)
    return message
