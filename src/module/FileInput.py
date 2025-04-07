import os


def random_n_bit_from_file(bit_size, file_name):
    try:
        with open(file_name, 'rb') as file:
            bits = []

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

                bits.append(binary_string)

            # Concatenate all the bits and truncate to the requested bit size
            bits = ''.join(bits)[:bit_size]

            # Convert the bits string to an integer
            print("Random bit successful:", bits)
            return int(bits, 2)
    except FileNotFoundError as ex:
        print(f"File not found: {ex}")
    except IOError as ex:
        print(f"IOException occurred: {ex}")
    return -1
