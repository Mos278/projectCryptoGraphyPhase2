def paddingBit(bit, block_size):
    while len(bit) < block_size:
        bit = '0' + bit
    return bit


def paddingToSizeForward(bit, size):
    for i in range(size):
        bit = '0' + bit
    return bit


def paddingToSizeBackward(bit, size):
    for i in range(size):
        bit = bit + '0'
    return bit


def removePaddingToCountBackward(bit, count):
    bit = bit[:len(bit) - count]
    return bit


def removePaddingForward(bit, block_size):
    return bit[len(bit) % block_size:]


def removePaddingBackward(bit, block_size):
    return bit[:len(bit) - (len(bit) % block_size)]