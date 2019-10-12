def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """

    l = "abcdefghijklmnopqrstuvwxyz"
    keyword = keyword.lower()
    b = -1
    ciphertext = ""
    for ch in plaintext:
        a = ord(ch)
        b += 1
        k = l.index(keyword[b % len(keyword)])
        if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'):
            if (('A' <= ch <= 'Z') and (chr (a + k) > 'Z')) or (('a' <= ch <= 'z') and (chr (a + k) > 'z')):
                a = a - 26
            a = chr (a + k)
            ciphertext += a
        else: 
            ciphertext += ch
        plaintext = plaintext.replace(ch, " ")
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """

    l = "abcdefghijklmnopqrstuvwxyz" 
    keyword = keyword.lower() 
    b = -1 
    plaintext = "" 
    for ch in ciphertext: 
        a = ord(ch) 
        b += 1 
        k = l.index(keyword[b % len(keyword)]) 
        if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'): 
            if (('A' <= ch <= 'Z') and (chr (a - k) < 'A')) or (('a' <= ch <= 'z') and (chr (a - k) < 'a')): 
                a = a + 26 
            a = chr (a - k) 
            plaintext += a 
        else: 
            plaintext += ch 
        ciphertext = ciphertext.replace(ch, " ")
    return plaintext