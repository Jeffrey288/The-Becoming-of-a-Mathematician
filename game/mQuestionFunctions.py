"""
mQuestionFunctions.py
"""

import random
import math
from fractions import *
from decimal import *
from mQuestionErrors import *

def FracValue(valLower, valUpper, numLower, numUpper):

    n, d, v = RandFraction(valLower, valUpper, numLower, numUpper)
    return v

def RandFraction(valLower, valUpper, numLower, numUpper):

    run = True
    while run:
        try:
            value = Decimal(RandomFloat(valLower, valUpper, 15))
            denominator = abs(RandomInt(numLower, numUpper))
            numerator = int(denominator * value)
            value = Fraction(numerator / denominator)
            hcf = HCF(denominator, numerator)
            denominator //= hcf
            numerator //= hcf
        except:
            pass
        else:
            if value:
                run = False

    return numerator, denominator, value

def RandomFloat(lower, upper, precision=3):

    num = math.ceil((lower + (upper - lower) * random.random()) * 10**precision) / 10**precision

    if num:
        return num
    else:
        return RandomFloat(lower, upper, precision)

def HCF(a, b):

    a = int(a)
    b = int(b)

    if a > b:
        a, b = b, a
    a = abs(a)
    b = abs(b)

    if a < 0 or b < 0:
        raise RangeError("a, b must be greater than 0!")

    rem = b % a
    if rem == 0:
        return a
    else:
        return HCF(rem, a)


def RandomInt(lower, upper, elower=0, eupper=0):

    if upper < lower:
        lower, upper = upper, lower

    if 0 in [lower,upper]:
        return random.randint(lower, upper)
    else:
        i = random.randint(lower, upper)
        while i == 0 or elower <= i <= eupper:
            i = random.randint(lower, upper)

    return i

def FractionRepresentation(n, d):

    f = Fraction(n/d).limit_denominator()
    n, d = f.numerator, f.denominator
    return str(n) + (("/" + str(d)) if d != 1 else "")