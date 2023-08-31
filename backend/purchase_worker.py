import asyncio

import redis

import purchase


redis_client = redis.asyncio.Redis(host="localhost", port=6379, db=0)


async def main() -> None:
    last_id_seen = "0"

    while True:
        # TODO: max stream size
        response = await redis_client.xread({purchase.Streams.purchase: last_id_seen})
        for stream_name, messages in response:
            for message_id, data in messages:
                last_id_seen = message_id

                purchase_info = purchase.PurchaseInfo.model_validate_json(data[b"data"])
                print(
                    f"{purchase_info.book_id=} {purchase_info.username=} | Processing"
                )
                await asyncio.sleep(5)
                print(f"{purchase_info.book_id=} {purchase_info.username=} | Done")

                await redis_client.xadd(purchase.Streams.purchase_processed, data)


if __name__ == "__main__":
    asyncio.run(main())
