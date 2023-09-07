import json
import asyncio
import os
from multiprocessing import Process

import redis
import uvicorn
from fastapi import FastAPI, Response, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise.queryset import QuerySet

import purchase
from models import Books, Books_Pydantic, BuyRequest, ListBooksCache, ListBooksResponse
from purchase_worker import order_worker


r = redis.asyncio.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=6379, db=0)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "https://redis-example.zat.ong"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def paginate(queryset: QuerySet, limit: int, offset: int) -> QuerySet:
    return queryset.order_by("id").offset(offset).limit(limit)


@app.on_event("startup")
async def add_background_workers():
    process = Process(target=order_worker)
    process.start()


@app.get("/status")
async def get_status():
    return {"ok": "ok"}


@app.get("/book/{book_id}", response_model=Books_Pydantic)
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
    details = json.loads(details)
    return Books_Pydantic(**details)


@app.get("/book", response_model=ListBooksResponse)
async def list_books(query: str = "", page_number: int = 0):
    cache_key = ListBooksCache.cache_key(query, page_number)
    if cache_result := await r.get(cache_key):
        return ListBooksCache.model_validate_json(cache_result).result

    # simulate heavy computations
    await asyncio.sleep(3)

    books_queryset = Books.filter(title__istartswith=query)
    response = ListBooksResponse(
        items=await Books_Pydantic.from_queryset(
            await paginate(books_queryset, 50, 50 * page_number)
        ),
        total_item_count=await books_queryset.count(),
    )

    await r.set(
        cache_key,
        ListBooksCache(
            result=response, query=query, page=page_number
        ).model_dump_json(),
        ex=40,
    )

    return response


@app.post("/book/{book_id}/buy")
async def buy_book(book_id: int, request: BuyRequest) -> None:
    purchase_info = purchase.PurchaseInfo(book_id=book_id, username=request.username)
    await r.rpush(purchase.WORKER_QUEUE_NAME, purchase_info.model_dump_json())
    await r.publish(
        purchase.WEBSOCKET_CHANNEL,
        purchase.WebsocketMessage(
            type=purchase.MessageTypes.purchase, data=purchase_info
        ).model_dump_json(),
    )


@app.websocket("/book/purchases")
async def purchases_websocket(websocket: WebSocket) -> None:
    await websocket.accept()

    pubsub = r.pubsub()
    await pubsub.subscribe(purchase.WEBSOCKET_CHANNEL)

    async for message in pubsub.listen():
        if message["type"] != "message":
            continue

        websocket_message = purchase.WebsocketMessage.model_validate_json(
            message["data"]
        )
        await websocket.send_json(websocket_message.model_dump())


register_tortoise(
    app,
    db_url="sqlite://db/bookdatabase.sqlite",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
