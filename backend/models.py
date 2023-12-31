from pydantic import BaseModel
from tortoise import fields, models
from tortoise.contrib.pydantic.creator import pydantic_model_creator


class Books(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    isbn = fields.CharField(max_length=20)
    author = fields.CharField(max_length=255)
    # pictures will be b64 encoded
    cover_picture = fields.TextField()


Books_Pydantic = pydantic_model_creator(Books, name="Book")


class ListBooksResponse(BaseModel):
    items: list[Books_Pydantic]
    total_item_count: int


class ListBooksCache(BaseModel):
    result: ListBooksResponse
    query: str
    page: int

    @staticmethod
    def cache_key(query: str, page: int) -> str:
        return f"book_search:{query.lower()}:{page}"


class BuyRequest(BaseModel):
    username: str
