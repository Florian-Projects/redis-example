from enum import Enum

from pydantic import BaseModel


WEBSOCKET_CHANNEL = 'websocket_messages'


class PurchaseInfo(BaseModel):
    username: str
    book_id: int


class MessageTypes(str, Enum):
    purchase = "purchase"
    purchase_processed = "purchase_processed"


class WebsocketMessage(BaseModel):
    type: MessageTypes
    data: PurchaseInfo
