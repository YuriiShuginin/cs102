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

    ciphertext = ""
    for ch in plaintext:
        a = ord(ch)
        if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'):
            if ('x' <= ch <= 'z') or ('X' <= ch <= 'Z'):
                a = a - 26
            a = chr(a + 3)
            ciphertext += a
        else: 
            ciphertext += ch
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

    plaintext = ""
    for ch in ciphertext:
        a = ord(ch)
        if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'):
            if ('a' <= ch <= 'c') or ('A' <= ch <= 'C'):
                a = a + 26
            a = chr(a - 3)
            plaintext += a
        else: 
            plaintext += ch
    return plaintext