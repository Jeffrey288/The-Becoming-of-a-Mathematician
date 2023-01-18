from random import *
from math import *

def appendPrime(num, coeff, coeffList):
    coeffList[num] = coeff

def q_a():
    '''
        'a' generates an integer from 1 to 10
        :return: int
    '''
    pass

def q_qra():
    '''
        'qra' generates three coefficients for a quadratic equation
        where the smallest denotes a and the largest denotes c
        for 'qra' to activate, there must be three consecutive
        digits with the 'qra' setting; otherwise, it has the
        same effect as 'a'
        :return: tuple of size 3
    '''
    # Generate three coefficients that satisfy b^2 - 4ac > 0
    # Should replace while loop with other methods
    found = False
    while not found:
        b = randint(5, 15)
        a = randint(1, 10)
        c = randint(1, 10)
        if b ** 2 - 4 * a * c > 0:
            found = True
    return a, b, c

def q_qrb():
    '''
        'qrb' generates the coefficients for a quadratic equations
        such that the roots are rational. The maximum value of the
        roots is 10
        :return: tuple of size 3
    '''

    return intRoot((1, 1), (1, 10), (1, 1), (1,10))

def intRoot(aTuple, bTuple, cTuple, dTuple):

    """ (ax + b)(cx + d) = ac x^2 + (bc + ad) x + bd """

    a = randint(aTuple[0], aTuple[1])
    b = randint(bTuple[0], bTuple[1])
    c = randint(cTuple[0], cTuple[1])
    d = randint(dTuple[0], dTuple[1])

    x = a * c
    y = b * c + a * d
    z = b * d

    return x, y, z