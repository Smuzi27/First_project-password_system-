from enum import IntEnum
from math import log2
import secrets

class StrenghtToEntropy(IntEnum):
    Pathetic = 0
    Weak = 32
    Good = 49
    Strong = 70
    Excellent = 120

def create_new(length: int, characters: str):
    return "".join(secrets.choice(characters) for _ in range(length))


def get_entropy(length: int, characters_number: int):
    try:
        entropy = length * log2(characters_number)
    except ValueError:
        return 0.0
    return round(entropy, 2)