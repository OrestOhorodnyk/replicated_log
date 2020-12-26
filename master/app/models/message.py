from typing import Optional

from pydantic import BaseModel, Field


class MessageOut(BaseModel):
    id: int
    message: str
    created_at: str

    def __key(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, MessageOut):
            return self.__key() == other.__key()
        return NotImplemented

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.id < other.id


class MessageIn(BaseModel):
    id: Optional[int] = Field(
        None, title="Id to use in message for ordering and deduplication"
    )
    message: str
    write_concern: int
