import sys

from . import GCD
from . import Exponentiation
from . import PrimeNumber
from . import FileInput
from . import Generator
from . import FileOutput
from . import ConvertDataType
from . import Padding
from . import HashFunction
from src.model import ElgamalKey

import random


def genSafePrime(bit_size, file_name):
    print("Reading file...")
    temp_result = FileInput.randomNBitFromFile(bit_size, file_name)
    result = PrimeNumber.findSafePrime(temp_result, bit_size)
    return result


def elgamalKeyGen(bit_size, random_file):
    p = genSafePrime(bit_size, random_file)
    g = Generator.findGenerator(p)
    u = random.randint(1, p - 1)

    y = Exponentiation.fastExpoWithModulo(base=g, expo=u, mod=p)

    return ElgamalKey.ElgamalKey(p=p, g=g, y=y, u=u)


def elgamalEncrypt(p, g, y, binary_data):
    block_size = len(ConvertDataType.intToBinary(p))
    message_size = block_size - 1
    ciphertext = ""

    for i in range(0, len(binary_data), message_size):  # แยกทุก message_size บิต
        bit = binary_data[i:i + message_size]
        print(f"{bit} length = {len(bit)}")
        message = int(bit, 2)

        # สุ่มค่า k และตรวจสอบว่า coprime กับ p-1
        k = random.randint(2, p - 1)
        while not GCD.isCoprime(base=k, mod=p - 1):
            k = random.randint(2, p - 1)

        print(f"k: {k}")
        # คำนวณค่า a
        a = Exponentiation.fastExpoWithModulo(base=g, expo=k, mod=p)
        print(f"A before padding: {a} : {ConvertDataType.intToBinary(a)} ")
        a = Padding.paddingBit(ConvertDataType.intToBinary(a), block_size)
        print(f"A after padding: {ConvertDataType.binaryToInt(a)} : {a} ")

        ciphertext += a

        # คำนวณ b
        b = (Exponentiation.fastExpoWithModulo(base=y, expo=k, mod=p) * message) % p
        print(f"B before padding: {b} : {ConvertDataType.intToBinary(b)} ")
        b = Padding.paddingBit(ConvertDataType.intToBinary(b), block_size)
        print(f"B after padding: {ConvertDataType.binaryToInt(b)} : {b} ")

        print("----------------------------------------")
        ciphertext += b

    print(f"Encrypt Success: {ciphertext} \nlength: {len(ciphertext)}")
    return ciphertext


def elgamalDecrypt(u, p, binary_cipher_text):
    block_size = len(ConvertDataType.intToBinary(p))
    message_size = block_size - 1
    cipher_size = block_size * 2
    before_last_block = len(binary_cipher_text) - cipher_size
    message = ""

    for i in range(0, before_last_block, cipher_size):
        bit = binary_cipher_text[i:i + cipher_size]
        a = bit[:block_size]
        b = bit[block_size:]

        a = ConvertDataType.binaryToInt(a)
        b = ConvertDataType.binaryToInt(b)
        print(f"A : {a} : {ConvertDataType.intToBinary(a)} ")
        print(f"B : {b} : {ConvertDataType.intToBinary(b)} ")

        s = Exponentiation.fastExpoWithModulo(a, u, p)
        temp_message = (b * GCD.findInverse(s, p)) % p
        temp_message = ConvertDataType.intToBinary(temp_message)
        temp_message = Padding.paddingBit(temp_message, message_size)
        print(f"message: {temp_message}")
        message += temp_message

    bit = binary_cipher_text[before_last_block:]
    a = bit[:block_size]
    b = bit[block_size:]

    a = ConvertDataType.binaryToInt(a)
    b = ConvertDataType.binaryToInt(b)
    print(f"A : {a} : {ConvertDataType.intToBinary(a)} ")
    print(f"B : {b} : {ConvertDataType.intToBinary(b)} ")

    s = Exponentiation.fastExpoWithModulo(a, u, p)
    temp_message = (b * GCD.findInverse(s, p)) % p
    temp_message = ConvertDataType.intToBinary(temp_message)
    missing_bits = 8 - ((len(message) + len(temp_message)) % 8)
    if missing_bits < 8:
        temp_message = Padding.paddingToSizeForward(temp_message, missing_bits)
    print(f"message: {temp_message}")
    message += temp_message

    print(f"Decrypt Success: {message} \nlength: {len(message)}")
    return message


def elgamalSignature(binary_data, p, g, u):
    block_size = len(ConvertDataType.intToBinary(number=p))
    print(f"----------------------------------------Start Sign----------------------------------------")
    hash_data = HashFunction.rwHash(binary_data=binary_data, p=p)
    hash_data_int = int(hash_data, 16)

    while True:
        k = random.randint(2, p - 2)
        if GCD.findGCD(k, p - 1) == 1:
            break

    r = Exponentiation.fastExpoWithModulo(base=g, expo=k, mod=p)
    k_inv = GCD.findInverse(k, p - 1)
    s = ((hash_data_int - u * r) * k_inv) % (p - 1)
    r = ConvertDataType.intToBinary(r)
    s = ConvertDataType.intToBinary(s)

    r = Padding.paddingBit(bit=r, block_size=block_size)
    s = Padding.paddingBit(bit=s, block_size=block_size)

    result = r + s
    binary_data += result
    print(f"----------------------------------------End Sign----------------------------------------")

    return binary_data


def elgamalVerification(sign_cipher_text, p, g, y):
    print(f"----------------------------------------Start verify----------------------------------------")
    binary_sign, binary_data = splitSignAndDataCipherText(binary_data=sign_cipher_text, p=p)
    block_size = len(binary_sign) // 2
    r = binary_sign[:block_size]
    r = ConvertDataType.binaryToInt(r)
    s = binary_sign[block_size:]
    s = ConvertDataType.binaryToInt(s)
    hash_data = HashFunction.rwHash(binary_data=binary_data, p=p)
    hash_data_int = int(hash_data, 16)
    if not (0 < r < p and 0 < s < p - 1):
        print("cipher text is non valid")
        return False
    a = (Exponentiation.fastExpoWithModulo(base=y, expo=r, mod=p) * Exponentiation.fastExpoWithModulo(
        base=r, expo=s, mod=p)) % p
    b = Exponentiation.fastExpoWithModulo(base=g, expo=hash_data_int, mod=p)

    print(f"verify -> hash(a): {a} == hash(b): {b}?")
    result = (a == b)
    if a == b:
        print(f"Verification is pass.")
    else:
        print(f"Verification is wrong")
    print(f"----------------------------------------End verify----------------------------------------")

    return result, binary_data


def splitSignAndDataCipherText(binary_data, p):
    block_size = len(ConvertDataType.intToBinary(p))
    cipher_size = block_size * 2  # a + b
    last_block_position = len(binary_data) - cipher_size
    sign = binary_data[last_block_position:]
    pure_data = binary_data[:last_block_position]

    return sign, pure_data
