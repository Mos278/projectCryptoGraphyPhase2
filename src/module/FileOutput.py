from . import ConvertDataType
from . import Padding


def writeBinaryToFile(binary_data, output_file_path):
    with open(output_file_path, 'wb') as file:
        number = ConvertDataType.binaryToInt(binary_string=binary_data)
        byte = ConvertDataType.intTobyte(number=number)

        file.write(byte)


def writeStringToFile(binary_data, output_file_path):
    with open(output_file_path, 'w') as file:
        file.write(binary_data)


def writeBinaryToFileHandlePostPadding(binary_data, output_file_path):
    print(f"write binary before padding : {binary_data}\nlength: {len(binary_data)}")
    binary_data = '1' + binary_data
    missing_bits = 8 - (len(binary_data) % 8)  # Cypher file support

    if missing_bits < 8:
        binary_data = Padding.paddingToSizeBackward(binary_data, missing_bits)
    print(f"write binary after padding: {binary_data}\nlength: {len(binary_data)}")

    with open(output_file_path, 'wb') as file:
        binary_data = ConvertDataType.binaryToInt(binary_string=binary_data)
        binary_data = ConvertDataType.intTobyte(binary_data)

        file.write(binary_data)


def saveKeyTofile(key, public_key_path, private_key_path, public_key_receiver_path=None):
    with open(public_key_path, 'w') as file:
        file.write(f"{key.p},{key.g},{key.y}")

    if public_key_receiver_path is not None:
        with open(public_key_receiver_path, 'w') as file:  # self sender receiver
            file.write(f"{key.p},{key.g},{key.y}")

    with open(private_key_path, 'w') as file:
        file.write(f"{key.p},{key.u}")

