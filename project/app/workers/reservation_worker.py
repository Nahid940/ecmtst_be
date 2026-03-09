import asyncio
import json
import redis.asyncio as redis

from app.database.database import async_session
from app.models.product import Product

redis_client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)


async def reservation_listener():

    pubsub = redis_client.pubsub()

    await pubsub.psubscribe("__keyevent@0__:expired")

    async for message in pubsub.listen():

        key = message["data"]

        # Normalize the key to string
        if isinstance(key, bytes):
            key = key.decode()
        elif isinstance(key, int):
            key = str(key)
        elif not isinstance(key, str):
            continue  # ignore other types

        if key.startswith("reservation:"):

            reservation_data = await redis_client.get(key)

            if reservation_data is None:
                continue

            data = json.loads(reservation_data)

            async with async_session() as db:
                product = await db.get(Product, data["product_id"])

                if product:
                    product.available_inventory += data["quantity"]
                    await db.commit()
