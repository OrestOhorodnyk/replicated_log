import logging
from app.models.message import Message

logger = logging.getLogger(__name__)


class MsgList(object):
    __messages = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MsgList, cls).__new__(cls)
        return cls.instance

    def add_msg(self, msg: Message):
        self.__messages.append(msg)
        logger.info(f'message added: "{msg}"')

    def get_messages(self) -> list:
        return self.__messages
