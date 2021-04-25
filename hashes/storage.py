import logging
import redis
import settings
from enum import Enum

redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

logging.basicConfig(format=settings.FORMAT)
logger = logging.getLogger('storage')

class RetStatus(Enum):
    STORED=0
    SKIPPED=1
    COLLISION=2

def redis_save(id: str, hash: int) -> RetStatus:
    existing = redis.get(f"HST:ID:{id}")
    if existing:
        return RetStatus.SKIPPED
    
    collision = redis.get(f"HST:HASH:{hash}")
    if collision:
        return RetStatus.COLLISION

    logger.debug("Wrote: id: %s, Hash: %s", id , hash)
    redis.set(f"HST:HASH:{hash}", id)
    redis.set(f"HST:ID:{id}", hash)
    return RetStatus.STORED
