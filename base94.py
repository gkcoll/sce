'''
@File    :   base94.py
@Time    :   2023/11/26 10:35:51
@Author  :   @灰尘疾客
@Version :   1.0
@Site    :   https://www.gkcoll.xyz
@Desc    :   Conversion between base 94 (self-created) and decimal.
'''

# The following code is a realization of conversion between decimal to base 94.
# The convert operation just support integer part.
# Code refer to: https://blog.csdn.net/jaket5219999/article/details/110209428


# Default character set. Length 94 (All printable character in ASCII)
chars = ''.join([chr(i) for i in range(33, 127)])


def b94(dec: int, char_set: str = chars) -> str:
    '''
    Function:
        Decimal to base 94.
    '''
    if dec == 0:
        return "0"
    r = []
    while dec > 0:
        r.append(char_set[dec % 94])
        dec //= 94
    return "".join(r[::-1])


def d94(s: str, char_set: str = chars) -> int:
    '''
    Function:
        Base 94 to decimal.
    '''
    dec = 0
    for char in s:
        dec = dec * 94 + char_set.index(char)
    return dec
