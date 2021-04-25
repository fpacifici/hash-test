from typing import Iterable, Tuple
from cityhash import CityHash64
import uuid

def generate() -> Iterable[Tuple[str, int]]:
    while True:
        unique_id = str(uuid.uuid4())
        hash = CityHash64(unique_id)
        yield (unique_id, hash)
