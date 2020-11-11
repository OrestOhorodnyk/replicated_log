from fastapi import APIRouter

from app.msg_manager import MsgManager
from app.message_model import Message

router = APIRouter()
msg_manager = MsgManager()


@router.get("/status")
async def status():
    return {"status": "OK"}


@router.get("/list_msg")
async def list_msg():
    return msg_manager.get_messages()


@router.post("/append_msg")
async def append_msg(msg: dict):
    message = Message(**msg)
    msg_manager.add_msg(message)
    return {"list size": len(msg_manager.get_messages())}
