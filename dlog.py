from math import gcd, sqrt
from operator import add, mul


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def bold_text(text):
    return color.BOLD + str(text) + color.END


def order(element, modulus):
    for n in range(1, modulus):
        if pow(element, n, modulus) == 1:
            return n
    else:
        return 0


def _table(op, modulus):
    width = len(str(modulus)) + 1
    fstr = '{:>' + str(width) + '}'

    print(fstr.format(' '), end='')
    for h in range(modulus):
        print(bold_text(fstr.format(h)), end='')
    print()

    for x in range(modulus):
        print(bold_text(fstr.format(x)), end='')
        for y in range(modulus):
            result = op(x, y) % modulus
            print(fstr.format(result), end='')
        print()


def multiplication_table(modulus):
    _table(mul, modulus)


def addition_table(modulus):
    _table(add, modulus)


def coprimes(n):
    cs = set()

    for i in range(n):
        if gcd(i, n) == 1:
            cs.add(i)

    return cs


def divisors(n):
    ds = set()

    for d in range(1, int(sqrt(n)) + 1):
        if n % d == 0:
            ds.add(d)
            ds.add(n//d)

    return ds


def euler_phi(n):
    k = 0

    for i in range(1, n+1):
        if gcd(i, n) == 1:
            k += 1

    return k


def generators(n):
    phi = euler_phi(n)
    gs = set()

    for g in range(n):
        if order(g, n) == phi:
            gs.add(g)

    return gs


def generators2(n):
    for g in range(2, n):
        if is_primitive_root_even_better(g, n):
            yield g


def is_prime(n):
    if n < 2:
        return False
    else:
        for d in range(2, int(sqrt(n))+1):
            if n % d == 0:
                return False
        else:
            return True


def prime_factors(n):
    return {d for d in range(1, n) if n % d == 0 and is_prime(d)}


def is_primitive_root(g, p):
    generated_elements = [pow(g, i, p) for i in range(1, p)]
    return sorted(generated_elements) == list(range(1, p))


def is_primitive_root_better(g, p):
    for i in range(1, p-1):
        if pow(g, i, p) == 1:
            return False
    else:
        return True


def is_primitive_root_even_better(g, p):
    for d in prime_factors(p-1):
        if pow(g, (p-1)//d, p) == 1:
            return False
    else:
        return True


def dlog(root, modulus, value):
    for i in range(modulus):
        if pow(root, i, modulus) == value:
            return i
    else:
        return None
