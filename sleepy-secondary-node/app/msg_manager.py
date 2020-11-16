import logging
from app.message_model import Message

logger = logging.getLogger(__name__)


class MsgManager(object):
    __messages = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MsgManager, cls).__new__(cls)
        return cls.instance

    def add_msg(self, msg: Message):
        self.__messages.append(msg)
        logger.info(f'message added: "{msg}"')

    def get_messages(self) -> list:
        return self.__messages
