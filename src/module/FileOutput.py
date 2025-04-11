from . import ConvertDataType
from . import Padding


def writeBinaryToFile(binary_data, output_file_path):
    with open(output_file_path, 'wb') as file:
        binary_data = ConvertDataType.BinaryToB(binary_string=binary_data)

        file.write(binary_data)


def writeBinaryToFileHandlePostPadding(binary_data, output_file_path):
    print(f"write binary before padding : {binary_data}\nlength: {len(binary_data)}")
    missingBits = 8 - (len(binary_data) % 8)  # Cypher file support

    if missingBits < 8:
        binary_data = Padding.paddingToSizeBackward(binary_data, missingBits)
    print(f"write binary after padding: {binary_data}\nlength: {len(binary_data)}")

    with open(output_file_path, 'wb') as file:
        binary_data = ConvertDataType.BinaryToInt(binary_string=binary_data)
        binary_data = ConvertDataType.intTobyte(binary_data)

        file.write(binary_data)
