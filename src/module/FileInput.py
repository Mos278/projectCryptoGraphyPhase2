import os
from . import ConvertDataType
from . import Padding
from src.model import PublicKey
from src.model import PrivateKey


def randomNBitFromFile(bit_size, file_name):
    try:
        with open(file_name, 'rb') as file:
            bits = ''

            first_bit = True
            while len(bits) < bit_size:
                byte_read = file.read(1)

                if not byte_read:
                    break

                byte = byte_read[0]
                binary_string = ConvertDataType.intToBinary(byte)
                if first_bit:
                    binary_string = binary_string.lstrip('0')
                    first_bit = False

                bits += binary_string

            bits = ''.join(bits)[:bit_size]

            if len(bits) != bit_size:
                raise Exception("cannot set bits")

            print("Random bit successful:", bits)
            return int(bits, 2)
    except FileNotFoundError as ex:
        print(f"File not found: {ex}")
    except IOError as ex:
        print(f"IOException occurred: {ex}")
    return -1


def readBinaryFromFile(input_file_name):
    with open(input_file_name, 'rb') as file:
        data = file.read()

    binary_data = ConvertDataType.bytesToBinary(data)

    print(f"read file -> binary Data: {binary_data}\nlength: {len(binary_data)}")
    return binary_data


def readStringFromFile(input_file_name):
    with open(input_file_name, 'r') as file:
        data = file.read()
    print(f"read file -> Data: {data}")
    return data


def readBinaryFromFileHandlePostPadding(input_file_name, block_size):
    with open(input_file_name, 'rb') as file:
        data = file.read()

    binary_data = ConvertDataType.bytesToBinary(data)

    print(f"read file -> binary Data: {binary_data}\nlength: {len(binary_data)}")
    binary_data = binary_data[1:]
    binary_data = Padding.removePaddingBackward(bit=binary_data, block_size=block_size)
    print(f"remove padding -> binary Data: {binary_data}\nlength: {len(binary_data)}")

    return binary_data


def readPublicKeyFromFile(public_key_path):
    with open(public_key_path, 'r') as file:
        data = file.read()

    temp = [int(x) for x in data.split(',')]
    return PublicKey.PublicKey(p=temp[0], g=temp[1], y=temp[2])


def readPrivateKeyFromFile(private_key_path):
    with open(private_key_path, 'r') as file:
        data = file.read()

    temp = [int(x) for x in data.split(',')]
    return PrivateKey.PrivateKey(p=temp[0], u=temp[1])
