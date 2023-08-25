import json
import redis
from fastapi import FastAPI, Response
from tortoise.contrib.fastapi import register_tortoise
from models import Books, Books_Pydantic

r = redis.Redis(host='localhost', port=6379, db=0)
app = FastAPI()


@app.get("/status")
async def get_status():
    return {"ok": "ok"}

@app.get("/books/all")
async def get_all_books(response_model=list[Books_Pydantic]):
    books = await Books_Pydantic.from_queryset(Books.all())
    return books

@app.get("/books/")
async def get_specific_book(book_id: int, response: Response, response_model=Books_Pydantic):
    key = f"book:{book_id}"
    details = r.get(key)
    if not details:
        if book := await Books.filter(id=book_id).first():
            book_pydantic = await Books_Pydantic.from_tortoise_orm(book)
            r.set(key, book_pydantic.model_dump_json())
            return book_pydantic 
        else:
            response.status_code = 404
            return {}
    print("cached")
    details = json.loads(details)
    return Books_Pydantic(**details)


register_tortoise(
    app,
    db_url="sqlite://bookdatabase.sqlite",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
