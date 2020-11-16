from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    message: str
    created_at: datetime = datetime.utcnow()
