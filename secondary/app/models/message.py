from pydantic import BaseModel


class Message(BaseModel):
    id: int
    message: str
    created_at: str

    def __key(self):
        return self.id, self.message, self.created_at

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.__key() == other.__key()
        return NotImplemented

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.id < other.id
