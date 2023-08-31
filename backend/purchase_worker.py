import redis

import purchase

from time import sleep

redis_client = redis.Redis(host="localhost", port=6379, db=0)


def order_worker() -> None:
    while True:
        try:
            queue_name, response = redis_client.blpop(purchase.WORKER_QUEUE_NAME)
            purchase_info = purchase.PurchaseInfo.model_validate_json(response)
            sleep(5)
            message = purchase.WebsocketMessage(
                type=purchase.MessageTypes.purchase_processed, data=purchase_info
            )
            redis_client.publish(purchase.WEBSOCKET_CHANNEL, message.model_dump_json())
        except Exception:
            continue
