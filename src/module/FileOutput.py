from . import ConvertDataType


def writeBinaryToFile(binary_data, output_file_path):
    with open(output_file_path, 'wb') as file:
        binary_data = ConvertDataType.BinaryToInt(binary_string=binary_data)
        binary_data = ConvertDataType.intTobyte(binary_data)

        file.write(binary_data)
