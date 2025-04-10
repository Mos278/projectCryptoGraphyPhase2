def intToBinary(number):
    return bin(number)[2:]


def BinaryToInt(binary_string):
    return int(binary_string, 2)


def intTobyte(number):
    bytes_data = number.to_bytes((number.bit_length() + 7) // 8, 'big')
    return bytes_data


def bytesToBinary(byte_data):
    binary_data = ''.join(format(byte, '08b') for byte in byte_data)
    return binary_data


def strToBinary(string_data):
    return ''.join(format(ord(char), '08b') for char in string_data)


def binaryToStr(binary_string):
    # ตัดให้ลงตัวเป็น byte
    binary_string = binary_string[:len(binary_string) - len(binary_string) % 8]
    chars = [chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8)]
    return ''.join(chars)
