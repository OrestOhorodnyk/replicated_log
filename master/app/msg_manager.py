import logging
from app.models.message import MessageOut

logger = logging.getLogger(__name__)


class MsgManager:
    __messages = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MsgManager, cls).__new__(cls)
        return cls.instance

    def add_msg(self, msg: MessageOut):
        self.__messages.append(msg)
        logger.info(f'Message added to master node: "{msg}"')

    def get_messages(self) -> list:
        return self.__messages
