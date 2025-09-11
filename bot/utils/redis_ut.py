from init import redis_client


async def save_redis(
        key: str,
        value: int,
        ttl: int = 3600,
) -> None:
    await redis_client.set(name=key, value=value, ex=ttl)


async def key_exists(key: str) -> bool:
    return (await redis_client.exists(str(key))) > 0
