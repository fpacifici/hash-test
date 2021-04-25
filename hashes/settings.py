import os

FORMAT = '%(asctime)-15s %(message)s'

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = 6379
