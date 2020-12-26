import logging
from urllib.parse import urljoin
import json
import aiohttp
from fastapi import (
    APIRouter,
    HTTPException,
)
from fastapi_utils.tasks import repeat_every
from aiohttp.client_exceptions import ClientConnectorError
from app.constants import SECONDARIES_NODES

router_node = APIRouter()
logger = logging.getLogger(__name__)

session = None


@router_node.on_event('startup')
async def startup_event():
    global session
    timeout = aiohttp.ClientTimeout(total=5.0)     # override session timeout to 5 seconds instead 5 minutes
    session = aiohttp.ClientSession(timeout=timeout)
    logger.info("****************startup**************************")


@router_node.on_event("startup")
@repeat_every(seconds=5, logger=logger, wait_first=True)
async def get_node_status():
    for node in SECONDARIES_NODES:
        url = urljoin(f'http://{node["url"]}', 'status')
        try:
            async with session.get(url) as response:
                resp = await response.text()
                logger.debug(f'node name: {node["name"]}, status {resp}')
                resp_json = json.loads(resp)
                node['status'] = resp_json['status']
                logger.info(SECONDARIES_NODES)
        except ClientConnectorError as error:
            logger.error(error)
            if node['status'] == 'Healthy':
                node['status'] = 'Suspected'
            elif node['status'] == 'Suspected':
                node['status'] = 'Unhealthy'


def check_quorum():
    for node in SECONDARIES_NODES:
        if node['status'] != 'Healthy':
            raise HTTPException(
                status_code=500,
                detail=f"One or more nodes unavailable at the moment, please try again later"
            )
