import math
from . import Padding
from . import Exponentiation
from . import ConvertDataType


def rwHash(binary_data, p):
    print(f"input hash data: {binary_data}")
    block_size = math.floor(math.log2(p))
    print(f"log2p : {block_size}")
    h = 0
    vi = len(binary_data)

    missing_bits = block_size - (len(binary_data) % block_size)
    if missing_bits < block_size:
        binary_data = Padding.paddingToSizeBackward(binary_data, missing_bits)

    for i in range(0, len(binary_data), block_size):
        bits = binary_data[i:i+block_size]
        bits_int = ConvertDataType.binaryToInt(binary_string=bits)
        a = vi + bits_int
        b = Exponentiation.fastExpoWithModulo(base=a, expo=2, mod=p)
        c = b << 2
        h = c % p
        vi = h

    return hex(h)

