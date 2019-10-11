def is_prime(n: int) -> bool:
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    # PUT YOUR CODE HERE

    m = 0
    boo = bool()
    for i in range (1, (n+1)):
        if (n % i == 0):
            m += 1
    if m > 2:
        boo = False
    elif m == 2:
        boo = True
    return boo
    pass

def gcd(a: int, b: int) -> int:
    """
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    # PUT YOUR CODE HERE

    g = 0
    if a > b:
        for i in range(1, b+1):
            if (a % i == 0) and (b % i == 0):
                g = i
    elif a < b:
        for i in range(1, a+1):
            if (a % i == 0) and (b % i == 0):
                g = i
    else: g = a
    return g
    pass

def multiplicative_inverse(e: int, phi: int) -> int:
    """
    >>> multiplicative_inverse(7, 40)
    23
    """
    # PUT YOUR CODE HERE

    b = e
    a = phi
    arr = []
    x = 0
    y = 1
    while a % b != 0:
        arr.append(a // b)
        z = a
        a = b
        b = z % b
    for i in range(len(arr[::-1])):
           z = x
           x = y
           y = z - y * arr[i]
    d = y % phi
    return d
    pass

def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))