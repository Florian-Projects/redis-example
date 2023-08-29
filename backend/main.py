import json
import redis
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from models import Books, Books_Pydantic, SearchResponse

r = redis.Redis(host='localhost', port=6379, db=0)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
async def get_status():
    return {"ok": "ok"}


@app.get("/books/all", response_model=list[Books_Pydantic])
async def get_all_books():
    books = await Books_Pydantic.from_queryset(Books.all())
    return books


@app.get("/books/", response_model=Books_Pydantic)
async def get_specific_book(book_id: int, response: Response):
    key = f"book:{book_id}"
    details = await r.get(key)
    if not details:
        if book := await Books.filter(id=book_id).first():
            book_pydantic = await Books_Pydantic.from_tortoise_orm(book)
            await r.set(key, book_pydantic.model_dump_json())
            return book_pydantic
        else:
            response.status_code = 404
            return {}
    details = json.loads(details)
    return Books_Pydantic(**details)


@app.get("/books/search", response_model=list[SearchResponse])
async def search_book_by_title(q: str):
    key = f"book_search:{q}"
    search_result = await r.get(key)
    if not search_result:
        books = await Books_Pydantic.from_queryset(Books.filter(title__istartswith=q))
        search_result = [SearchResponse(**book.dict()) for book in books]
        await r.set(key, json.dumps(search_result))
        return search_result
    else:
        return json.loads(search_result)


register_tortoise(
    app,
    db_url="sqlite://bookdatabase.sqlite",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
