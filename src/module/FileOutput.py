from . import ConvertTypeData


def writeBinaryToFile(binary_data, output_file_name):
    with open(output_file_name, 'wb') as file:
        binary_data = ConvertTypeData.BinaryToInt(binary_string=binary_data)
        binary_data = ConvertTypeData.intTobyte(binary_data)

        file.write(binary_data)


def writeBinaryStringToFile(binary_data, output_file_name):
    with open(output_file_name, 'w') as file:
        # เขียนข้อมูล binary string ลงในไฟล์
        file.write(binary_data)
