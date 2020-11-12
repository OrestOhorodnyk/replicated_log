from fastapi import APIRouter
from datetime import datetime

from app.Replicator import replicate_message
from app.models.message import MessageOut, MessageIn
from app.msg_manager import MsgManager

router = APIRouter()
msg_manager = MsgManager()


@router.get("/status")
async def status():
    return {"status": "OK"}


@router.get("/list_msg")
async def list_msg():
    return msg_manager.get_messages()


@router.get("/list_size")
async def list_size():
    return {"list size": len(msg_manager.get_messages())}


@router.post("/append_msg", status_code=201, response_model=MessageOut)
async def append_msg(msg: MessageIn):
    message = MessageOut(message=msg.message, created_at=str(datetime.utcnow()))
    msg_manager.add_msg(message)
    await replicate_message(message)
    return message
