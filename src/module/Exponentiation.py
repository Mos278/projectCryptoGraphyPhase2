def fastExpo(base, expo):
    result = 1
    a = base
    b = expo

    while b > 0:
        if (b & 1) > 0:
            result = result * a
            if result <= 0:
                return -99  # overflow
        b >>= 1
        a = a * a
    return result


def fastExpoWithModulo(base, expo, mod):
    result = 1
    a = base
    b = expo

    while b > 0:
        if (b & 1) > 0:
            result = (result * a) % mod
            if result <= 0:
                return -99  # overflow
        b >>= 1
        a = (a * a) % mod
    return (result + mod) % mod
