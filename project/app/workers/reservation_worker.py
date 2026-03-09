import asyncio
import logging
import redis
import json
import os
from app.db import get_db  # your asyncpg/SQLAlchemy session

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
RESERVATION_PREFIX = "reservation:"


def start_expiry_listener():
    """
    Blocking pub/sub — runs in a background thread.
    Listens for expired Redis keys and restores product inventory.
    """
    r = redis.from_url(REDIS_URL, decode_responses=True)

    # Enable expiry events (safe to call on every startup)
    r.config_set("notify-keyspace-events", "Ex")

    pubsub = r.pubsub()
    pubsub.subscribe("__keyevent@0__:expired")

    logger.info("🚀 Worker listening for expired reservation keys...")

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        expired_key: str = message["data"]

        if not expired_key.startswith(RESERVATION_PREFIX):
            continue

        logger.info(f"🔔 Expired: {expired_key}")

        # Run async handler from sync thread
        asyncio.run(restore_inventory_from_key(expired_key, r))


async def restore_inventory_from_key(expired_key: str, redis_client):
    """
    Redis key has already expired — value is gone.
    We store a shadow copy in a separate hash to retrieve quantity + product_id.
    """

    # Retrieve reservation metadata from shadow hash
    shadow_key = f"shadow:{expired_key}"
    data = redis_client.hgetall(shadow_key)

    if not data:
        logger.warning(f"No shadow data found for {expired_key}, cannot restore")
        return

    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 0))

    if not product_id or quantity <= 0:
        logger.warning(f"Invalid shadow data for {expired_key}: {data}")
        return

    # Distributed lock — safe for multi-pod deployments
    lock_key = f"lock:expiry:{expired_key}"
    acquired = redis_client.set(lock_key, "1", nx=True, ex=30)
    if not acquired:
        logger.warning(f"Lock already held for {expired_key}, skipping")
        return

    try:
        async with get_db() as db:
            await db.execute(
                """
                UPDATE products
                SET available_quantity = available_quantity + $1,
                    updated_at = NOW()
                WHERE id = $2
                """,
                quantity,
                product_id,
            )
            logger.info(f"✅ Restored {quantity} units → product {product_id}")

        # Clean up shadow key after successful restore
        redis_client.delete(shadow_key)

    except Exception as e:
        logger.error(f"❌ Failed to restore inventory for {expired_key}: {e}",