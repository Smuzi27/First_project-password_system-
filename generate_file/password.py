from enum import IntEnum
from math import log2
import secrets


class StrenghtToEntropy(IntEnum):
    Pathetic = 0
    Weak = 32
    Good = 49
    Strong = 70
    Excellent = 120


def create_new(length, characters):
    return "".join(secrets.choice(str(characters)) for _ in range(int(length)))


def get_entropy(length, characters_number):
    try:
        entropy = int(length) * log2(int(characters_number))
    except ValueError:
        return 0.0
    return round(entropy, 2)
