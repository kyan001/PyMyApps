import math
import random
import binascii


def is_prime_6k(num: int):
    if num < 4:
        return num > 1
    if num % 2 == 0 or num % 3 == 0:
        return False
    for k in range(1, int(num ** 0.5 // 6) + 1):
        if num % (6 * k - 1) == 0 or num % (6 * k + 1) == 0:
            return False
    return True


def is_prime(num: int):
    if num < 4:
        return num > 1
    for i in range(2, int(num ** 0.5)):
        if num % i == 0:
            return False
    return True


def find_prime_number(length: int = 100):
    """
    Args:
        length: length in bits

    Returns:
        a prime number with requested bit length
    """
    while True:
        num = random.randint(2 ** (length - 1), 2 ** length)
        if is_prime(num):
            return num


def is_coprime(a: int, b: int):
    return math.gcd(a, b) == 1


def find_coprime_number(M: int):
    i = 2
    while True:
        if is_coprime(i, M):
            return i
        i += 1


def find_D(M, E: int = 65537):
    if not E:
        print("E is None")
        return None
    i = 1
    while True:
        D = (M * i + 1) // E
        if D == (M * i + 1) / E:
            return D
        i += 1


def main():
    P = find_prime_number(10)  # 100 bits long int.
    Q = find_prime_number(10)  # 100 bits long int.
    N = P * Q  # Public
    M = (P - 1) * (Q - 1)
    print("P:", P)
    print("Q:", Q)
    print("N:", N, "(Public Modulus)")
    print("M:", M)
    E = find_coprime_number(M)
    print("E:", E, "(Public Key)")
    D = find_D(M, E)
    print("D:", D, "(Private Key)")


if __name__ == "__main__":
    main()
