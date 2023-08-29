from pydantic import BaseModel


PURCHASE_STREAM = "purchase"


class PurchaseInfo(BaseModel):
    username: str
    book_id: int
