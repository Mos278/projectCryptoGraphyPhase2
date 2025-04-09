def findGCD(first, second):
    a = first
    b = second
    while b != 0:
        temp = a % b
        a = b
        b = temp
    return a


def isCoprime(base, mod):
    return findGCD(base, mod) == 1


def findInverse(a, p):
    # ค่าใด เมื่อ * กับ a เเล้ว p กับ modulo เเล้วได้เศษ 1

    if not isCoprime(a, p):
        print(f"{a} and {p} are not coprime")
        return -1

    original_p = p

    x0, x1 = 1, 0
    while p != 0:
        q = a // p
        temp = p
        p = a % p
        a = temp

        temp = x1
        x1 = x0 - q * x1
        x0 = temp

    if a != 1:
        return -1
    return (x0 + original_p) % original_p
