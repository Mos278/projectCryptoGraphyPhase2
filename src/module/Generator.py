import random

from . import PrimeNumber
from . import Exponentiation


def find_generator(p):
    # p is prime
    if PrimeNumber.isPrime(p):
        g = random.randint(1, p - 1)

        while g % p == 1 or g % p == (p - 1):
            g = random.randint(1, p - 1)

        if Exponentiation.fastExpoWithModulo(g, (p - 1) // 2, p) != 1:
            return g % p
        else:
            return (-g) % p

    else:
        history = set()

        while True:
            g = random.randint(1, p - 1)
            generator_not_found = True
            for i in range(1, p - 1):
                result = Exponentiation.fastExpoWithModulo(g, i, p)
                if result in history:
                    generator_not_found = False
                    break
                else:
                    history.add(result)
                    #Random new g in generator
            if generator_not_found: return g
