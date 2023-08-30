from enum import Enum

from pydantic import BaseModel


class Streams(str, Enum):
    purchase = "purchase"
    purchase_processed = "purchase_processed"


class PurchaseInfo(BaseModel):
    username: str
    book_id: int


class WebsocketMessage(BaseModel):
    type: Streams
    data: PurchaseInfo
