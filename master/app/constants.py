SECONDARIES_NODES = [
    # {"name": "secondary 1", "url": "localhost:8001", "status": "n/a"},
    # {"name": "secondary 2", "url": "localhost:8002", "status": "n/a"},
    {"name": "secondary 1", "url": "secondary-1:8000", "status": "n/a", "required": True},
    {"name": "secondary 2", "url": "secondary-2:8000", "status": "n/a", "required": False},
]


MESSAGE_REPLICATION_STATUS_FAILED = "failed"
MESSAGE_REPLICATION_STATUS_OK = "OK"
NUMBER_OF_MASTER_NODES = 1
NUMBER_OF_RETRY_TO_REPLICATE_MESSAGE = 500
MAX_DELAY_BEFORE_RETRY_SECONDS = 5
