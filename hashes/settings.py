import os

FORMAT = '%(asctime)-15s %(message)s'

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = 6379
