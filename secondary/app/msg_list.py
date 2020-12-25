import logging
import bisect
from app.models.message import Message

logger = logging.getLogger(__name__)


class MsgList:
    __messages = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MsgList, cls).__new__(cls)
        return cls.instance

    def add_msg(self, msg: Message):
        if msg not in self.__messages:
            bisect.insort(self.__messages, msg)
            logger.info(f'Message added: "{msg}"')
        else:
            logger.info(f'Message already exist: "{msg}"')

    def get_messages(self) -> list:
        return self.__messages
