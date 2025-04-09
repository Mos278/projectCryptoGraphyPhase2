import random

from . import Exponentiation
from . import GCD


class STATE_PRIME:
    PRIME = "PRIME"
    NOT_PRIME = "NOT_PRIME"
    OVERFLOW = "OVERFLOW"


def isPrime(number):
    if number == 2:
        return STATE_PRIME.PRIME
    if number % 2 == 0 or number < 2:
        return STATE_PRIME.NOT_PRIME

    candidates = [
        random.randint(1, number - 1)
        for _ in range(100)
        if GCD.findGCD(random.randint(1, number - 1), number) == 1
    ]

    for candidate in candidates:
        expo = Exponentiation.fastExpoWithModulo(candidate, (number - 1) // 2, number)
        result = expo % number

        if expo == -99:
            print(f"Overflow detected: number = {number}, candidate = {candidate}, Expo: {(number - 1) // 2}")
            return STATE_PRIME.OVERFLOW

        if result != 1 and result != -1 and result != number - 1:
            print(f"Not Prime detected: number = {number}, candidate = {candidate}, result = {result}")
            return STATE_PRIME.NOT_PRIME

    print(f"Prime detected: number = {number}")
    return STATE_PRIME.PRIME


def findSafePrime(number, bit):
    max_length = Exponentiation.fastExpo(2, bit) - 1
    min_length = Exponentiation.fastExpo(2, (bit - 1))
    ran = convertToOdd(number, max_length)

    while True:
        if isPrime(ran) != STATE_PRIME.PRIME:
            ran += 2
            if ran >= max_length:
                ran = convertToOdd(random.randint(min_length, max_length - 1), max_length)
            continue

        if not isSavePrime(ran):
            print(f"{ran} is not safe Prime")
            ran += 2
            if ran >= max_length:
                ran = convertToOdd(random.randint(min_length, max_length - 1), max_length)
            continue

        print(f"Safe Prime Found: {ran}")
        return ran


def convertToOdd(temp_result, max_value):
    if temp_result % 2 == 0:
        if temp_result == max_value:
            temp_result -= 1
        else:
            temp_result += 1
    return temp_result


def findMaxPrimeBeforeOverflow():
    max_prime = 0
    for i in range(3, 2 ** 63, 2):  # Loop through odd numbers
        state = isPrime(i)
        if state == STATE_PRIME.PRIME:
            max_prime = i
        if state == STATE_PRIME.OVERFLOW:
            break
    print(f"Max Prime Number = {max_prime}")
    return max_prime


def isSavePrime(p):
    if isPrime((p - 1) // 2) == STATE_PRIME.PRIME:
        return True
    return False
