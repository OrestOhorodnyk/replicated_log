import logging
from datetime import datetime

from fastapi import (
    APIRouter,
    HTTPException,
    BackgroundTasks,
)

from app.replicator import (
    replicate_to_minimum_required_nodes,
    replicate_to_the_rest_of_nodes,
)
from app.constants import (
    SECONDARIES_NODES,
    NUMBER_OF_MASTER_NODES,
)
from app.models.message import MessageOut, MessageIn
from app.msg_list import MsgList
from app.utils import ID_GENERATOR
from app.node.status_checker import check_quorum

router = APIRouter()
msg_list = MsgList()
logger = logging.getLogger(__name__)


@router.get("/status")
async def status():
    node_statuses = {}
    for node in SECONDARIES_NODES:
        node_statuses[node['name']] = {
            'status': node['status'],
            'url': node['url']
        }
        node_statuses.update({"master": {"status": "Healthy"}})
    return node_statuses


@router.get("/cluster-health")
async def cluster_health():
    return {"status": "OK"}


@router.get("/list_msg")
async def list_msg():
    return msg_list.get_messages()


@router.get("/list_size")
async def list_size():
    return {"list size": len(msg_list.get_messages())}


@router.post("/append_msg", status_code=201, response_model=MessageOut)
async def append_msg(msg: MessageIn, background_tasks: BackgroundTasks):
    check_quorum()
    message = MessageOut(
        id=msg.id if msg.id else next(ID_GENERATOR),
        message=msg.message,
        created_at=str(datetime.utcnow())
    )
    if msg.write_concern > (len(SECONDARIES_NODES) + NUMBER_OF_MASTER_NODES) or msg.write_concern <= 0:
        raise HTTPException(
            status_code=400,
            detail=f"Incorrect wright concern, can't replicate message to {msg.write_concern} nodes, "
                   f"{len(SECONDARIES_NODES) + NUMBER_OF_MASTER_NODES} nodes are available."
        )
    msg_list.add_msg(message)
    await replicate_to_minimum_required_nodes(message, msg.write_concern)
    replicate_to_the_rest_of_nodes(message, msg.write_concern, background_tasks)
    return message
