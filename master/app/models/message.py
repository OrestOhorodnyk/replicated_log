from pydantic import BaseModel


class MessageOut(BaseModel):
    message: str
    created_at: str


class MessageIn(BaseModel):
    message: str
    write_concern: int
