from enum import Enum

from pydantic import BaseModel

WEBSOCKET_CHANNEL = "websocket_messages"
WORKER_QUEUE_NAME = "order_queue"


class PurchaseInfo(BaseModel):
    username: str
    book_id: int


class MessageTypes(str, Enum):
    purchase = "purchase"
    purchase_processed = "purchase_processed"


class WebsocketMessage(BaseModel):
    type: MessageTypes
    data: PurchaseInfo
