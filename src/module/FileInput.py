import os
from . import ConvertDataType


class TYPE_READ:
    BIT = 'rb',
    INFILE = 'r'


def randomNBitFromFile(bit_size, file_name):
    try:
        with open(file_name, 'rb') as file:
            bits = ''

            first_bit = True
            while len(bits) < bit_size:
                byte_read = file.read(1)

                if not byte_read:
                    break  # End of file reached

                byte = byte_read[0]
                binary_string = f'{byte:08b}'  # Convert byte to binary string (8 bits)

                if first_bit:
                    # Remove leading zeros until the first '1' bit is found
                    binary_string = binary_string.lstrip('0')

                    # After finding the first '1', we continue processing
                    first_bit = False

                bits += binary_string

            # Concatenate all the bits and truncate to the requested bit size
            bits = ''.join(bits)[:bit_size]

            if len(bits) != bit_size:
                raise Exception("cannot set bits")

            # Convert the bits string to an integer
            print("Random bit successful:", bits)
            return int(bits, 2)
    except FileNotFoundError as ex:
        print(f"File not found: {ex}")
    except IOError as ex:
        print(f"IOException occurred: {ex}")
    return -1


def readBinaryFromInFile(input_file_name):
    with open(input_file_name, 'rb') as file:  # เปิดไฟล์ในโหมด binary
        data = file.read()  # อ่านข้อมูลในรูปแบบไบต์

    # แปลง byte data เป็น binary string
    binary_data = ''.join(f'{byte:08b}' for byte in data)

    print(f"read file -> binary Data: {binary_data}\nlength: {len(binary_data)}")  # แสดงข้อมูลในรูปแบบ binary
    return binary_data


def readBinaryFromFile(input_file_name):
    with open(input_file_name, 'rb') as file:  # เปิดไฟล์ในโหมด binary
        data = file.read()  # อ่านข้อมูลในรูปแบบไบต์

    # ไม่ทำการแปลงเป็น binary string แต่ให้เก็บข้อมูลเป็น byte ที่อ่านมา
    binary_data = ConvertDataType.bytesToBinary(data) # เก็บข้อมูลในรูปแบบ byte
    print(f"read file -> binary Data: {binary_data}\nlength: {len(binary_data)}")  # แสดงข้อมูลในรูปแบบ byte
    return binary_data  # คืนค่าเป็น byte string
