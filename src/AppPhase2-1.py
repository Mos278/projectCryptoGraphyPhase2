import sys

from module import GCD
from module import Exponentiation
from module import PrimeNumber
from module import FileInput
from module import Generator
from module import FileOutput
from module import ConvertDataType
from module import Padding
from model import ElgamalKey

import random
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')


def genSafePrime(bit_size, file_name):
    print("Reading file...")
    temp_result = FileInput.randomNBitFromFile(bit_size, file_name)
    result = PrimeNumber.findSafePrime(temp_result, bit_size)
    return result


def ElgamalKeyGen(bit_size, random_file):
    p = genSafePrime(bit_size, random_file)
    g = Generator.findGenerator(p)
    u = random.randint(1, p - 1)

    y = Exponentiation.fastExpoWithModulo(base=g, expo=u, mod=p)

    return ElgamalKey.ElgamalKey(p=p, g=g, y=y, u=u)


def ElgamalEncrypt(p, g, y, binary_file):
    block_size = len(ConvertDataType.intToBinary(p))
    message_size = block_size - 1
    ciphertext = ""

    for i in range(0, len(binary_file), message_size):  # แยกทุก message_size บิต
        bit = binary_file[i:i + message_size]
        print(f"{bit} length = {len(bit)}")
        message = int(bit, 2)

        # สุ่มค่า k และตรวจสอบว่า coprime กับ p-1
        k = random.randint(2, p - 1)
        while not GCD.isCoprime(base=k, mod=p - 1):
            k = random.randint(2, p - 1)

        # คำนวณค่า a
        a = Exponentiation.fastExpoWithModulo(base=g, expo=k, mod=p)
        print(f"A before padding: {a} : {ConvertDataType.intToBinary(a)} ")
        a = Padding.paddingBit(ConvertDataType.intToBinary(a), block_size)
        print(f"A after padding: {ConvertDataType.BinaryToInt(a)} : {a} ")

        ciphertext += a

        # คำนวณ b
        b = (Exponentiation.fastExpoWithModulo(base=y, expo=k, mod=p) * message) % p
        print(f"B before padding: {b} : {ConvertDataType.intToBinary(b)} ")
        b = Padding.paddingBit(ConvertDataType.intToBinary(b), block_size)
        print(f"B after padding: {ConvertDataType.BinaryToInt(b)} : {b} ")

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

        a = ConvertDataType.BinaryToInt(a)
        b = ConvertDataType.BinaryToInt(b)
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

    a = ConvertDataType.BinaryToInt(a)
    b = ConvertDataType.BinaryToInt(b)
    print(f"A : {a} : {ConvertDataType.intToBinary(a)} ")
    print(f"B : {b} : {ConvertDataType.intToBinary(b)} ")

    s = Exponentiation.fastExpoWithModulo(a, u, p)
    temp_message = (b * GCD.findInverse(s, p)) % p
    temp_message = ConvertDataType.intToBinary(temp_message)
    missingBits = 8 - ((len(message) + len(temp_message)) % 8)
    if missingBits < 8:
        temp_message = Padding.paddingToSizeForward(temp_message, missingBits)
    print(f"message: {temp_message}")
    message += temp_message

    print(f"Decrypt Success: {message} \nlength: {len(message)}")
    return message


def main():
    bit_size = int(config['config_elgamal']["bit_size"])
    random_file_path = config['random_file']['path']
    input_file_path = config['input_file']['path']
    cipher_file_path = config['cipher_file']['path']
    output_file_path = config['output_file']['path']

    #Set Up
    key = ElgamalKeyGen(bit_size=bit_size, random_file=random_file_path)

    #Encrypt
    binary_input_file = FileInput.readBinaryFromFile(input_file_name=input_file_path)
    print(f"input length: {len(binary_input_file)}")
    cipher_text = ElgamalEncrypt(p=key.p, g=key.g, y=key.y, binary_file=binary_input_file)
    FileOutput.writeBinaryToFileHandlePostPadding(binary_data=cipher_text, output_file_path=cipher_file_path)

    #Decrypt
    binary_cipher_text_read_from_file = FileInput.readBinaryFromFileHandlePostPadding(input_file_name=cipher_file_path,
                                                                                      block_size=bit_size)
    message = elgamalDecrypt(u=key.u, p=key.p, binary_cipher_text=binary_cipher_text_read_from_file)
    FileOutput.writeBinaryToFile(binary_data=message, output_file_path=output_file_path)


if __name__ == "__main__":
    main()
