'''
@File    :  vigenere.py
@Time    :  2023/03/19 13:37:36
@Author  :  @灰尘疾客
@Site    :  https://www.gkcoll.xyz
@Desc    :  A Vigenere cipher algorithm that adapted to full character set,
            modified from English-adapted version.
'''

chars = ''.join([chr(i) for i in range(33, 127)])


def filt(text: str, char_set: str = chars) -> list:
    '''
    Function:
        A customize filter, scan all valid character to encrypt.
    '''
    return [char for char in text if char in char_set]


def legality(obj: str, char_set) -> bool:
    '''
    Function:
        Check legality. If all character in obj also included in char_set, 
    return True, else raise an exception.
    '''
    if sum([1 for i in obj if i in char_set]) != len(obj):
        raise Exception('Found illegal character in `obj`!')
    return True


def complete_key(text: str, char_set, key: str) -> str:
    '''
    Function:
        Repeat key until the length same as text.
    '''
    legality(key, char_set)
    length = len(filt(text))
    key = key * (length // len(key)) + key[:length % len(key)]
    return key


def get_cipher(k: str, t: str, c: str) -> str:
    '''
    Function:
    Calculate and get the cipher character (encrypted) of target character.

    Parameters Description:
    - k: The key
    - t: The target character
    - c: The character set
    '''
    return c[(c.index(t) + c.index(k)) % len(c)]


def get_clear(k: str, t: str, c: str) -> str:
    '''
    Function:
    Calculate and get the clear character (decrypted) of target character.

    Parameters Description:
    - k: The key
    - t: The target character
    - c: The character set
    '''
    return c[(c.index(t) - c.index(k)) % len(c)]


def encrypt(plaintext: str, key: str, char_set: str = chars) -> str:
    '''
    Function:
        Encryption function of this high-customize Vigenere algorithm.
    '''
    chars = filt(plaintext)
    key = complete_key(chars, char_set, key)
    groups = list(zip(chars, key))

    ciphetext = ""
    for i in plaintext:
        if i not in chars:
            ciphetext += i
        else:
            ciphetext += get_cipher(groups[0][1], groups[0][0], char_set)
            del groups[0]

    return ciphetext


def decrypt(ciphertext: str, key: str, char_set: str = chars) -> str:
    '''
    Function:
        Decryption function of this high-customize Vigenere algorithm.
    '''
    chars = filt(ciphertext)
    key = complete_key(ciphertext, char_set, key)
    groups = list(zip(chars, key))

    cleartext = ""
    for i in ciphertext:
        if i not in chars:
            cleartext += i
        else:
            cleartext += get_clear(groups[0][1], groups[0][0], char_set)
            del groups[0]

    return cleartext