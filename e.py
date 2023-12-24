'''
@File    :   e.py
@Time    :   2023/08/17 11:42:47
@Author  :   @灰尘疾客
@Site    :   https://www.gkcoll.xyz
@Desc    :   Calculate the base of the Natural Logarithms - e.
'''

from fractions import Fraction as F
from decimal import Decimal as D
from decimal import getcontext
from math import factorial as f



def calc(step: int, prec: int = 300):
    '''
    Function:
        Calculate constant e to specified precision.
    '''
    getcontext().prec = prec
    e = 2
    for i in range(2, step + 1):
        e += F(1, f(i))
    # Convert Fraction to Decimal directly is not supported.
    return str(D(e.numerator) / D(e.denominator))


def get(index: int, step: int, prec: int = 300):
    '''
    Function:
        Get digit on specified position.
    '''
    const_e = calc(step, prec)
    try:
        return const_e[index]
    except IndexError:
        return const_e[-1]
