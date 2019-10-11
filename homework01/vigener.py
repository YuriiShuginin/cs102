def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # PUT YOUR CODE HERE

    l = "abcdefghijklmnopqrstuvwxyz"
    keyword = keyword.lower()
    b = -1
    ciphertext = ""
    for i in plaintext:
        a = ord(i)
        b += 1
        k = l.index(keyword[b % len(keyword)])
        if (64 < a < 91) or (96 < a < 123):
            if ((64 < a < 91) and (a + k > 90)) or ((96 < a < 123) and (a + k > 122)):
                a = a - 26
            a = chr (a + k)
            ciphertext += a
        else: ciphertext += i
        plaintext = plaintext.replace(i, " ")
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
    # PUT YOUR CODE HERE

    l = "abcdefghijklmnopqrstuvwxyz" 
    keyword = keyword.lower() 
    b = -1 
    plaintext = "" 
    for i in ciphertext: 
        a = ord(i) 
        b += 1 
        k = l.index(keyword[b % len(keyword)]) 
        if (64 < a < 91) or (96 < a < 123): 
            if ((64 < a < 91) and (a - k < 65)) or ((96 < a < 123) and (a - k < 97)): 
                a = a + 26 
            a = chr (a - k) 
            plaintext += a 
        else: plaintext += i 
    ciphertext = ciphertext.replace(i, " ")
    return plaintext