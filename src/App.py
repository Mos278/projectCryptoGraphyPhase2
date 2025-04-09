from module import GCD
from module import Exponentiation
from module import PrimeNumber
from module import FileInput
from module import Generator

import random


def gen_prime(bit, file_name):
    print("Reading file...")
    temp_result = FileInput.randomNBitFromFile(bit, file_name)

    forward = True
    max_value = (Exponentiation.fastExpo(2, bit) - 1)
    min_value = Exponentiation.fastExpo(2, bit - 1)
    round_count = 0
    first_backward = True

    result_odd = convertToOdd(temp_result, max_value)
    print(f"Result random from file: {result_odd}")
    temp_result_odd = result_odd

    while PrimeNumber.isPrime(result_odd) == 'NOT_PRIME':
        round_count += 1
        if forward and result_odd + 2 < max_value:
            result_odd = result_odd + 2
        elif result_odd - 2 > min_value:
            forward = False
            if first_backward:
                result_odd = temp_result_odd - 2
                first_backward = False
            else:
                result_odd = result_odd - 2
        else:
            raise Exception("Cannot find Prime Number")

        print(f"Result from Gen Prime: {result_odd} round: {round_count}")

    return result_odd


def gen_random_no_with_inverse(n):
    e = random.randint(1, n - 1)

    while GCD.findGCD(e, n) != 1:
        e += 1
        if e >= n:
            e = 1

    inverse = GCD.findInverse(e, n)

    return [e, inverse, n]


def convertToOdd(temp_result, max_value):
    if temp_result % 2 == 0:
        if temp_result == max_value:
            temp_result -= 1
        else:
            temp_result += 1
    return temp_result


def ElgamalKeyGen(p):
    if PrimeNumber.isSavePrime(p):
        u = random.randint(1, p - 1)
        g = Generator.findGenerator(p)


def main():
    randomPrimeNumber = gen_prime(64, "../resource/img.png")
    result = gen_random_no_with_inverse(randomPrimeNumber)
    print(f"base: {result[0]}  inverse:  + {result[1]} +  prime:  + {result[2]}")
    print((result[0] * result[1]) % result[2])


if __name__ == "__main__":
    main()
