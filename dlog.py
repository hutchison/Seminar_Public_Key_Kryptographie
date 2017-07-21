from math import gcd, sqrt
from operator import add, mul
from typing import List, Tuple
from itertools import combinations


def dlog_naive(modulus, root, value):
    """
    Berechnet den diskreten Logarithmus auf naive Weise.

    >>> dlog_naive(13, 2, 5)
    9
    >>> dlog_naive(1801, 13, 111)
    1768
    """

    for x in range(1, modulus):
        if pow(root, x, modulus) == value:
            return x
    else:
        return None


def factorize(n):
    """
    Bestimmt die Primfaktorzerlegung von n und gibt ein Dictionary mit den
    Primfaktoren und den dazugehörigen Exponenten zurück.

    >>> factorize(2)
    {2: 1}
    >>> factorize(4)
    {2: 2}
    >>> factorize(100)
    {2: 2, 5: 2}
    """

    F = dict()

    while n > 1:
        for p in range(2, n+1):
            if n % p == 0:
                if p not in F:
                    F[p] = 1
                else:
                    F[p] += 1
                n = n // p
                break

    return F


def roots_of_unity(modulus, root, factorization):
    r = dict()

    for q in factorization:
        r[q] = [pow(root, j*(modulus-1) // q, modulus) for j in range(q)]

    return r


def generating_list(p, xs):
    """
    Berechnet
        x_0 + p * x_1 + p**2 * x_2 + …
    für x_i ∈ xs.

    Der Name lehnt sich an die Erzeugendenfunktionen (generating functions) an.

    >>> generating_list(2, [])
    0
    >>> generating_list(2, [1])
    1
    >>> generating_list(2, [1, 2])
    5
    """
    r = 0

    for i, x in enumerate(xs):
        r += x * p**i

    return r


def dlog_ph(modulus, root, value):
    """
    Berechnet den diskreten Logarithmus nach dem Pohlig-Hellman-Algorithmus.

    >>> dlog_naive(1801, 13, 111)
    1768
    """
    F = factorize(modulus-1)
    r = roots_of_unity(modulus, root, F)
    inv = modular_inverse(root, modulus)
    congruences = []

    for q in F:
        exp = F[q]
        cs = []
        y = value

        for i in range(exp):
            v = pow(y, (modulus-1) // q**(i+1), modulus)
            c = r[q].index(v)
            cs.append(c)

            y = (y * pow(inv, c * q**i, modulus)) % modulus

        crt_modulus = q**exp
        congruences.append(
            (generating_list(q, cs), crt_modulus)
        )

    return crt(congruences)


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
    """
    Bestimmt die Ordnung eines Elements mod `modulus`.

    >>> order(2, 3)
    2
    """
    for n in range(1, modulus):
        if pow(element, n, modulus) == 1:
            return n
    else:
        return 0


def _table(op, modulus, start=0):
    width = len(str(modulus)) + 1
    fstr = '{:>' + str(width) + '}'

    print(fstr.format(' '), end='')
    for h in range(start, modulus):
        print(bold_text(fstr.format(h)), end='')
    print()

    for x in range(start, modulus):
        print(bold_text(fstr.format(x)), end='')
        for y in range(start, modulus):
            result = op(x, y) % modulus
            print(fstr.format(result), end='')
        print()


def multiplication_table(modulus):
    _table(mul, modulus, start=1)


def addition_table(modulus):
    _table(add, modulus)


def coprimes(n):
    """
    Bestimmt die Menge der zu n teilerfremden Zahlen.

    >>> coprimes(3)
    {1, 2}
    >>> coprimes(4)
    {1, 3}
    """
    cs = set()

    for i in range(n):
        if gcd(i, n) == 1:
            cs.add(i)

    return cs


def divisors(n):
    """
    Bestimmt die Menge aller Teiler von n.

    >>> divisors(2)
    {1, 2}
    >>> divisors(4)
    {1, 2, 4}
    >>> divisors(6)
    {1, 2, 3, 6}
    """
    ds = set()

    for d in range(1, int(sqrt(n)) + 1):
        if n % d == 0:
            ds.add(d)
            ds.add(n//d)

    return ds


def are_coprime(a: int, b: int) -> bool:
    """
    Bestimmt, ob a und b teilerfremd sind.

    >>> are_coprime(2, 3)
    True
    >>> are_coprime(2, 4)
    False
    """
    return gcd(a, b) == 1


def extended_gcd(a: int, b: int) -> Tuple[int, int]:
    """
    Bestimmt zu a und b die Zahlen s und t, für die gcd(a, b) == a*s + b*t
    gilt.

    >>> extended_gcd(99, 78)
    (-11, 14)
    """
    if b == 0:
        return (1, 0)
    else:
        (q, r) = divmod(a, b)
        (s, t) = extended_gcd(b, r)
        return (t, s-q*t)


def modular_inverse(a: int, modulus: int) -> int:
    (s, _) = extended_gcd(a, modulus)
    return s % modulus


def crt(congruences: List[Tuple[int, int]]) -> int:
    """
    Sei congruences eine Liste von Zahlenpaaren:
        [(a_1, m_1), (a_2, m_2), …]
    dann löst die Funktion mittels Chinesischem Restsatz das System linearer
    Kongruenzen:
        x ≡ a_1 mod m_1
        x ≡ a_2 mod m_2
        ⋮

    >>> crt([(2, 3), (3, 4), (2, 5)])
    47
    """

    """
    Zuerst checken wir, ob die Eingabedaten in Ordnung sind:
    """
    assert {len(t) for t in congruences} == {2}, (
        'Eins der Tupel hat nicht die Länge 2!'
    )

    """
    Die Moduli m_1, m_2, … müssen alle relativ prim sein:
    """
    moduli = [m for (_, m) in congruences]
    for i, j in combinations(moduli, 2):
        assert are_coprime(i, j), 'Zwei Moduli sind nicht relativ prim!'

    """
    Auf geht's mit dem Finden der Lösung.

    Erst berechnen wir M = m_1 * m_2 * …
    """
    M = 1
    for m in moduli:
        M *= m

    """
    Und dann zu jedem m_i:
        M_i = M / m_i
    """
    coprime_ms = [M // m_i for m_i in moduli]
    assert len(moduli) == len(coprime_ms), (
        'Jetzt ist richtig was in die Hose gegangen. '
        'moduli und coprime_ms sind nicht gleich lang!'
    )

    """
    Jetzt bestimmten wir die multiplikativen Inversen zu jedem (m_i, M_i)
    Pärchen (diese existieren, weil m_i und M_i teilerfremd sind).
    """
    inverses = []
    for m_i, M_i in zip(moduli, coprime_ms):
        _, s = extended_gcd(m_i, M_i)
        e = s * M_i
        inverses.append(e)

    """
    Und jetzt können wir schon die Lösung berechnen:
        x = a_1 * e_1 + a_2 * e_2 + …
    wobei die e_i alle aus inverses sind.
    """
    x = 0
    rests = [a for (a, _) in congruences]
    for a, e in zip(rests, inverses):
        x += a * e

    """
    Wir geben die Lösung zurück, die aus [0, M) ist:
    """
    return x % M


def euler_phi(n: int) -> int:
    """
    Die Eulersche φ-Funktion.

    >>> euler_phi(2)
    1
    >>> euler_phi(3)
    2
    >>> euler_phi(4)
    2
    >>> euler_phi(13)
    12
    """
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
    gs = set()

    for g in range(1, n):
        if is_primitive_root_even_better(g, n):
            gs.add(g)

    return gs


def is_prime(n):
    """
    Ein einfacher Primzahltest.

    >>> is_prime(-1)
    False
    >>> is_prime(0)
    False
    >>> is_prime(1)
    False
    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    >>> is_prime(4)
    False
    >>> is_prime(5)
    True
    """
    if n < 2:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    else:
        for d in range(3, int(sqrt(n))+1, 2):
            if n % d == 0:
                return False
        else:
            return True


def is_strong_prime(n):
    return is_prime(n) and is_prime((n-1)//2)


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


def powers(root, modulus, start=1):
    width = len(str(modulus)) + 1
    width_root = len(str(root))
    fstr = '{:>' + str(width) + '}'

    print(bold_text((width_root+2)*' ' + 'n:'), end='')
    for n in range(start, modulus):
        print(bold_text(fstr.format(n)), end='')

    print()

    print(bold_text(fstr.format(str(root) + '**n:')), end='')
    for n in range(start, modulus):
        print(fstr.format(pow(root, n, modulus)), end='')


def encode_char(c):
    if c == ' ':
        return 27
    else:
        return ord(c.upper()) - ord('A') + 1


def encode_text(text):
    return [encode_char(c) for c in text]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
