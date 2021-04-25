from typing import Iterable, Tuple
from cityhash import CityHash64
import uuid
from math import floor
import random

def generate_uuids() -> Iterable[Tuple[str, int]]:
    while True:
        unique_id = str(uuid.uuid4())
        hash = CityHash64(unique_id)
        yield (unique_id, hash)

START = 65
END = 122
ALPHABET = [
    chr(i) for i in range(START, START + END + 1)
]

def generate_strings() -> Iterable[Tuple[str, int]]:
    pos = 0
    while True:
        pos += random.randint(1, 1000)
        shift = pos
        ret = []
        while shift > 0:
            ret.insert(0, ALPHABET[shift % (END - START)])
            shift = floor(shift / (END - START))
        id = "".join(ret)
        yield (id, CityHash64(id))
