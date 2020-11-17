from pydantic import BaseModel


class Message(BaseModel):
    message: str
    created_at: str
