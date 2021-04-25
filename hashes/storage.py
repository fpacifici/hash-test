import logging
import redis
import settings
from enum import Enum
import psycopg2

redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
postgres = psycopg2.connect(f"dbname=hashes user=postgres host={settings.POSTGRES_HOST}")
logging.basicConfig(format=settings.FORMAT)
logger = logging.getLogger('storage')

init=False

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

def postgres_save(id: str, hash: int) -> RetStatus:
    global init
    if not init:
        cursor = postgres.cursor()
        sql = "CREATE TABLE IF NOT EXISTS hashes (id varchar(4096) PRIMARY KEY, hash NUMERIC)"
        cursor.execute(sql)
        sql = "CREATE UNIQUE INDEX IF NOT EXISTS hash_idx ON hashes (hash)"
        cursor.execute(sql)
        postgres.commit()
        cursor.close()
        init = True
    
    with postgres.cursor() as cursor:
        cursor.execute(f"SELECT id from hashes where id ='{id}'")
        if cursor.fetchone():
            return RetStatus.SKIPPED
        
        cursor.execute(f"SELECT id from hashes where hash ={hash}")
        exist_id = cursor.fetchone()
        if exist_id:
            return RetStatus.COLLISION
        
        cursor.execute("INSERT INTO hashes (id, hash) VALUES (%s, %s)", (id, hash)),
        logger.debug("Wrote: id: %s, Hash: %s", id , hash)
        postgres.commit()
        return RetStatus.STORED
