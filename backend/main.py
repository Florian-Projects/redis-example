import json
import redis
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise.queryset import QuerySet
from models import Books, Books_Pydantic, SearchResponse

r = redis.asyncio.Redis(host='localhost', port=6379, db=0)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def paginate(queryset: QuerySet, limit: int, offset: int) -> QuerySet:
    return queryset.order_by("id").offset(offset).limit(limit)


@app.get("/status")
async def get_status():
    return {"ok": "ok"}


@app.get("/book/", response_model=Books_Pydantic)
async def get_specific_book(book_id: int, response: Response):
    key = f"book:{book_id}"
    details = await r.get(key)
    if not details:
        if book := await Books.filter(id=book_id).first():
            book_pydantic = await Books_Pydantic.from_tortoise_orm(book)
            await r.set(key, book_pydantic.model_dump_json(), ex=40)
            return book_pydantic
        else:
            response.status_code = 404
            return {}
    else:
        await r.expire(key, 40)
    details = json.loads(details)
    return Books_Pydantic(**details)


@app.get("/book/search", response_model=list[SearchResponse])
async def search_book_by_title(q: str, page_number: int = 0):
    q = q.lower()
    key = f"book_search:{q}:{page_number}"
    search_result = await r.get(key)
    if not search_result:
        books = await Books_Pydantic.from_queryset(
            await paginate(Books.filter(title__istartswith=q), 50, 50 * page_number))
        search_result = json.dumps([SearchResponse(**book.dict()).model_dump_json() for book in books])
        await r.set(key, search_result, ex=40)

    else:
        await r.expire(key, 40)

    return [SearchResponse(**json.loads(rsp)) for rsp in json.loads(search_result)]


register_tortoise(
    app,
    db_url="sqlite://bookdatabase.sqlite",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
