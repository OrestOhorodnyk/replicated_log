from datetime import datetime
from dataclasses import dataclass


@dataclass
class Message:
    message: str
    created_at: datetime = datetime.utcnow()