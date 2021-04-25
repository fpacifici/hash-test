from generators import generate_strings
import logging
from logging import INFO
from storage import redis_save, postgres_save, RetStatus
import settings

logging.basicConfig(format=settings.FORMAT)
logger = logging.getLogger('storage')
logger.setLevel(INFO)

progress = 0
stored = 0
skipped = 0
collisions = 0
for id, hash in generate_strings():
    ret = redis_save(id, hash)
    progress += 1
    if ret == RetStatus.STORED:
        stored += 1
    elif ret == RetStatus.SKIPPED:
        skipped += 1
    else:
        collisions += 1
    
    if progress % 50 == 0:
        logger.info("Last: %s, Stored %d, Skipped %d, Collisions %d", id, stored, skipped, collisions)
