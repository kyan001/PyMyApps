'''This Program is due to varify the ID number is valid of not.

https://daily.zhihu.com/story/9729532
'''
import consoleiotools as cit

WEIGHT = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1)


def get_id_str() -> str:
    while True:
        cit.ask("Please Enter ID Number:")
        id_str = cit.get_input()
        if len(id_str) == 18:
            return id_str
        else:
            cit.err("ID number must be 18 digits!")


def get_id_ints(id_str: str) -> list:
    id_strs = list(id_str)
    if id_strs[-1].lower() == 'x':
        id_strs[-1] = '10'
    return list(map(int, id_strs))


def get_products_sum(id_ints: list) -> bool:
    # products = list(map(lambda x, y: x * y, id_ints, WEIGHT))
    products = [x * w for x, w in zip(id_ints, WEIGHT)]
    return sum(products)


def get_mod_11(products_sum: int) -> int:
    return products_sum % 11


def main():
    id_str = get_id_str()
    cit.info(f"ID: {id_str}")
    id_ints = get_id_ints(id_str)
    cit.info(f"ID: {id_ints}")
    products_sum = get_products_sum(id_ints)
    cit.info(f"WEIGHT: {WEIGHT}")
    cit.info(f"ID Digits Products Sum: {products_sum}")
    mod = get_mod_11(products_sum)
    cit.info(f"Mod 11 Result: {mod}")
    is_valid = mod == 1
    if is_valid:
        cit.info(f"This ID is VALID!")
    else:
        cit.warn(f"This ID is NOT VALID!")


if __name__ == '__main__':
    main()
