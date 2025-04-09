import random

from . import PrimeNumber
from . import Exponentiation


def findGenerator(sp):
    # sp is safe Prime
    g = random.randint(1, sp - 1)

    while g % sp == 1 or g % sp == (sp - 1):
        g = random.randint(1, sp - 1)

    if Exponentiation.fastExpoWithModulo(g, (sp - 1) // 2, sp) != 1:
        result = g % sp
    else:
        result = (-g) % sp

    print(f"find generator: {result}")
    return result
