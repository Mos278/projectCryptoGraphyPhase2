import os
from . import ConvertDataType


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
