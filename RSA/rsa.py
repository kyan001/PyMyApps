import math
import random
import binascii


def find_prime_number(length: int = 100):
    """
    Args:
        length: length in bits

    Returns:
        a prime number with requested bit length
    """
    def is_prime(num: int):
        for i in range(2, num // 2):
            if num % i == 0:
                return False
        return True

    while True:
        num = random.randint(2 ** (length - 1), 2 ** length)
        if is_prime(num):
            return num

def find_coprime_number(M: int):
    i = 2
    while True:
        if math.gcd(i, M) == 1:
            return i
        i += 1


def find_D(M, E):
    if not E:
        print("E is None")
        return None
    i = 1
    while True:
        D = (M * i + 1) // E
        if D == (M * i + 1) / E:
            return D
        i += 1


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

X = input("Enter your word: ")
X_ascii = int.from_bytes(binascii.b2a_hex(bytes(X), byteorder="big")

