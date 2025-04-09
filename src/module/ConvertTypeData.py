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
