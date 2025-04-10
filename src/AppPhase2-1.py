import sys

from module import GCD
from module import Exponentiation
from module import PrimeNumber
from module import FileInput
from module import Generator
from module import FileOutput
from module import ConvertTypeData
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


def genInverseByRandomNumber(n):
    e = random.randint(1, n - 1)

    while GCD.findGCD(e, n) != 1:
        e += 1
        if e >= n:
            e = 1

    inverse = GCD.findInverse(e, n)

    return [e, inverse, n]


def ElgamalKeyGen(bit_size, random_file):
    p = genSafePrime(bit_size, random_file)
    g = Generator.findGenerator(p)
    u = random.randint(1, p - 1)

    y = Exponentiation.fastExpoWithModulo(base=g, expo=u, mod=p)

    return ElgamalKey.ElgamalKey(p=p, g=g, y=y, u=u)


def ElgamalEncrypt(p, g, y, binary_file):
    block_size = len(ConvertTypeData.intToBinary(p))  #กำหนด p เป็น block_size

    # เก็บ ciphertext ในรูปของ list
    ciphertext = ""

    # ทำการเข้ารหัสแต่ละข้อความ
    for i in range(0, len(binary_file), block_size):  # แยกทุก block_size บิต
        # แปลง binary string เป็น integer
        bit = binary_file[i:i + block_size]
        print(f"{bit} length = {len(bit)}")
        message = int(bit, 2)

        # สุ่มค่า k และตรวจสอบว่า coprime กับ p-1
        k = random.randint(2, p - 1)
        while not GCD.isCoprime(base=k, mod=p - 1):
            k = random.randint(2, p - 1)

        # คำนวณค่า a
        a = Exponentiation.fastExpoWithModulo(base=g, expo=k, mod=p)
        print(f"A before padding: {a} : {ConvertTypeData.intToBinary(a)} ")
        a = paddingBit(ConvertTypeData.intToBinary(a), block_size)
        print(f"A after padding: {ConvertTypeData.BinaryToInt(a)} : {a} ")

        ciphertext += a

        # คำนวณ b
        b = (Exponentiation.fastExpoWithModulo(base=y, expo=k, mod=p) * message) % p
        print(f"B before padding: {b} : {ConvertTypeData.intToBinary(b)} ")
        b = paddingBit(ConvertTypeData.intToBinary(b), block_size)
        print(f"B after padding: {ConvertTypeData.BinaryToInt(b)} : {b} ")

        print("----------------------------------------")
        ciphertext += b

    print(f"Encrypt Success: {ciphertext} \nlength: {len(ciphertext)}")
    return ciphertext  # คืนค่า ciphertext ที่ได้


def paddingBit(bit, block_size):
    while len(bit) < block_size:
        bit = '0' + bit
    return bit


def removePadding(bit, block_size):
    return bit[len(bit) % block_size:]


def elgamalDecrypt(u, p, binary_cipher_text):
    block_size = len(ConvertTypeData.intToBinary(p))  # กำหนดขนาดของ block
    cipher_size = block_size * 2
    message = ""  # ตัวแปรที่เก็บข้อความที่ถอดรหัสแล้ว

    for i in range(0, len(binary_cipher_text), cipher_size):  # แยกทุก block_size บิต
        bit = binary_cipher_text[i:i + cipher_size]
        a = bit[:block_size]  # แยกส่วนของ a
        b = bit[block_size:]  # แยกส่วนของ b

        a = ConvertTypeData.BinaryToInt(a)
        b = ConvertTypeData.BinaryToInt(b)
        print(f"A : {a} : {ConvertTypeData.intToBinary(a)} ")
        print(f"B : {b} : {ConvertTypeData.intToBinary(b)} ")

        s = Exponentiation.fastExpoWithModulo(a, u, p)
        temp_message = (b * GCD.findInverse(s, p)) % p
        # temp_message = b * (Exponentiation.fastExpoWithModulo(base=a, expo=(p-1-u),mod= p))
        temp_message = ConvertTypeData.intToBinary(temp_message)
        # temp_message = paddingBit(bit=temp_message, block_size=block_size)
        # padding_message = paddingBit(bit=temp_message, block_size=block_size)
        print(f"message: {temp_message}")
        message += temp_message

    print(f"Decrypt Success: {message} \nlength: {len(message)}")
    return message


def main():
    # test()
    bit_size = int(config['config_elgamal']["bit_size"])
    random_file_path = config['random_file']['path']
    input_file_path = config['input_file']['path']
    cipher_file_path = config['cipher_file']['path']
    output_file_path = config['output_file']['path']

    binary_string = "0110100001100101011011000110110001101111001000000111011101101111011100100110110001100100"
    #Set Up
    key = ElgamalKeyGen(bit_size=bit_size, random_file=random_file_path)
    print(f"binary: {binary_string}\nlength: {len(binary_string)}")

    #Encrypt
    # binary_input_file = FileInput.readBinaryFromInFile(input_file_name=input_file_path)
    cipher_text = ElgamalEncrypt(p=key.p, g=key.g, y=key.y, binary_file=binary_string)
    # FileOutput.writeBinaryToFile(binary_data=cipher_text, output_file_name=cipher_file_path)
    #
    # #Decrypt
    # binary_cipher_text_read_from_file = FileInput.readBinaryFromFile(input_file_name=cipher_file_path)
    # binary_cipher_text_read_from_file = removePadding(bit=binary_cipher_text_read_from_file, block_size=bit_size)
    # print(f"bit: {binary_cipher_text_read_from_file}\nlength: {len(binary_cipher_text_read_from_file)}")
    message = elgamalDecrypt(u=key.u, p=key.p, binary_cipher_text=cipher_text)
    # print("---------------------------------")
    # for item in message:
    #     print(item)
    # FileOutput.writeBlocksToFile(data=message, sp_bit_length=key.p, output_filename=config['output_file']['path'])


if __name__ == "__main__":
    main()
