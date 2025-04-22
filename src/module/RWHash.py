from . import ConvertDataType
from . import Padding
from . import Exponentiation


def HWHash(message, p):
    bit_size = len(ConvertDataType.intToBinary(p))
    block_size = bit_size - 1
    message_size = len(message)
    hash_temp = 0

    missing_bits = block_size - (message_size % block_size)
    if missing_bits < block_size:
        message = Padding.paddingToSizeBackward(message, missing_bits)

    for i in range(0, len(message), block_size):
        bit = message[i:i + block_size]
        # print(f"{bit} length = {len(bit)}")
        block_value = ConvertDataType.binaryToInt(bit)
        if i == 0:
            hash_temp = message_size
        hash_temp = hash_temp + block_value
        hash_temp = Exponentiation.fastExpoWithModulo(hash_temp, 2, p)
        hash_temp = (hash_temp << 2) % p

    hash_value = ConvertDataType.decimalToHex(hash_temp)
    return hash_value
