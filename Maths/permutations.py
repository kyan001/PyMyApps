def arrangement(n: int, m: int = None) -> int:  # A_n^m
    if m is None:
        return a(n, n)
    if m > n or m < 1 or n < 1:
        raise ValueError(f"1 <= {m} <= {n} does not satisfied")
    if m == 1:
        return n
    return arrangement(n, m - 1) * (n - m + 1)


a = arrangement


def combination(n: int, m: int) -> int:  # C_n^m
    if m is None:
        return a(n, n)
    if m > n or m < 1 or n < 1:
        raise ValueError(f"1 <= {m} <= {n} does not satisfied")
    if m == 1:
        return n
    return combination(n, m - 1) * (n - m + 1) // m


c = combination
