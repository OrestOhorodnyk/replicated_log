from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Message:
    message: str
    created_at: str = field(init=False, default_factory=lambda: str(datetime.utcnow()))
