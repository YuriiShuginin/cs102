def encrypt_caesar(plaintext: str) -> str:
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE

    for i in plaintext:
        a=ord(i)
        if (64 < a < 123):
            if (87 < a < 91) or (119 < a < 123):
                a = a - 26
            a = chr(a + 3)
            plaintext = plaintext.replace(i, a)
    ciphertext = plaintext
    return ciphertext


def decrypt_caesar(ciphertext: str) -> str:
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE

    for i in ciphertext:
        b=ord(i)
        if (64 < b < 123):
            if (64 < b < 68) or (96 < b < 100):
                b = b + 26
            b = chr(b - 3)
            ciphertext = ciphertext.replace(i, b)
    plaintext = ciphertext
    return plaintext