from fastapi import APIRouter

from app.msg_manager import MsgManager
from app.models.message import Message
from app.Replicator import replicate_message
router = APIRouter()
msg_manager = MsgManager()


@router.get("/")
async def read_root():
    return {"Hello": "World"}


@router.get("/list_msg")
async def list_msg():
    return msg_manager.get_messages()


@router.post("/append_msg", status_code=201)
async def append_msg(msg: dict):
    message = Message(msg.get("message"))
    msg_manager.add_msg(message)
    await replicate_message(message)
    return {"list size": len(msg_manager.get_messages())}
