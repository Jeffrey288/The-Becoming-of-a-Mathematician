"""
mQuestionObjects.py
"""


import random
import math
import re
from fractions import *
from decimal import *
from mQuestionFunctions import *
from mQuestionErrors import *
import GlobalVar

DISPLAYUNICODE = GlobalVar.SettingDict["Unicode"]

switch = {
        "randint" : "RANDINT",
        "fraction" : "FRACTION",
        "randfloat" : "RANDFLOAT",
        "as" : "AS",
        "array" : "ARRAY",
        "eval" : "EVAL",
        "multias" : "MULTIAS",
        "gs" : "GS",
        "quadratic" : "QUADRATIC",
        "polynomial" : "POLYNOMIAL"
    }

def StrToBool(string):
    if isinstance(string, str):
        if string.lower() == "true":
            return True
        else:
            return False
    else:
        return string

def ArgsString(args):

    if len(args) == 1:
        argsString = "(" + str(args[0]) + ")"
    else:
        argsString = str(tuple(args))
    return argsString


def ExecuteFunction(obj, function, args):
    if function in ["eval", "evalRandStr", "validate"]:
        args = ",".join(args)
        return getattr(obj, function)(args)
    else:
        return getattr(obj, function)(*args)

class EVAL:

    def __init__(self):
        pass

    def eval(self, string):
        return eval(string)

    def evalInt(self, string, max = 10000000):
        inta = eval(string)
        max = int(max)
        if abs(inta) > max:
            raise RangeError("Fraction too large. Regeneration is required.")
        return inta

    def evalFloat(self, string):
        return eval(string)

    def evalFraction(self, string, vmax = 100000, dmax = 50000):

        try:
            f = Fraction(eval(string)).limit_denominator()
        except:
            f = Fraction(string).limit_denominator()

        n = f.numerator
        d = f.denominator
        vmax = int(vmax)
        dmax = int(dmax)
        if (abs(d) > dmax and n != 1) or abs(n) > dmax or abs(f) > vmax:
            raise FractionError
        if d == 1:
            return str(f.numerator)
        else:
            return str(f.numerator) + "/" + str(f.denominator)

    def evalRand(self, lower, upper, elower = 0, eupper = 0):
        return RandomInt(int(lower), int(upper), int(elower), int(eupper))

    def evalRandStr(self, strList):
        strList = strList.strip("()")
        return re.split(",", strList)[random.randrange(len(re.split(",", strList)))]

    def validate(self, condition):
        try:
            if eval(condition):
                return ""
            else:
                raise ValidationError
        except:
            raise ValidationError

    def varDisplay(self, coeff, exponent = '1', sign = False, space = False, varName = "x", vmax = 100000, dmax = 50000):

        self.evalFraction(coeff, vmax = vmax, dmax = dmax)

        sign = StrToBool(sign)
        space = StrToBool(space)

        showSign = sign
        showSpace = space
        n = int(exponent)
        if DISPLAYUNICODE:
            unicodeDict = {
                '0' : '\u2070',
                '1' : '\u2071',
                '2' : '\u00B2',
                '3' : '\u00B3',
                '4' : '\u2074',
                '5' : '\u2075',
                '6' : '\u2076',
                '7' : '\u2077',
                '8' : '\u2078',
                '9' : '\u2079'
            }
            displayN = ""
            for i in exponent:
                displayN += unicodeDict[i]
        else:
            displayN = '^' + exponent


        coeff = Fraction(self.evalFraction(coeff))

        if len(varName) > 1:
            varName = "(" + varName + ")"

        varName = (varName + (displayN if n != 1 else "") if n else "")
        f = Fraction(coeff).limit_denominator()
        numCoeff = str(abs(f.numerator)) if (abs(f.numerator) != 1 or n == 0) else ""
        denCoeff = ("/" + str(abs(f.denominator))) if f.denominator != 1 else ""
        space = ""

        if float(f) != 0:
            if int(coeff) == coeff:
                if showSpace:
                    return ("- " if coeff < 0 else ("+ " if showSign else "")) + numCoeff + varName + space
                else:
                    return ("-" if coeff < 0 else ("+" if showSign else "")) + numCoeff + varName + space
            else:
                if showSpace:
                    return ("- " if coeff < 0 else ("+ " if showSign else "")) + numCoeff + varName + denCoeff + space
                else:
                    return ("-" if coeff < 0 else ("+" if showSign else "")) + numCoeff + varName + denCoeff + space
        else:
            return ""



class ARRAY:

    # Add "" when specifying objType
    # No need to add "" when specifying attr

    def __init__(self, objType, num, args):

        self.array = []
        valArray = []

        if objType in ["randint", "randfloat", "fraction"]:

            for i in range(num):
                fin = False
                count = 0
                while not fin:
                    tempObj = eval(switch[objType] + ArgsString(args))
                    if tempObj.value not in valArray:
                        self.array.append(tempObj)
                        valArray.append(tempObj.value)
                        fin = True
                    else:
                        count += 1
                        if count > 50:
                            raise ArrayError

                self.sortedArray = sorted(self.array, key=lambda x: x.value, reverse=False)
        else:
            raise RangeError

    def sortedAttr(self, n, attr):

        n = int(n)

        return getattr(self.sortedArray[n], attr)

    def attr(self, n, attr):

        n = int(n)

        return getattr(self.array[n], attr)

    def func(self, n, func, args):

        n = int(n)

        return ExecuteFunction(self.array[n], func, args)


class RANDINT:

    def __init__(self, lower, upper, elower=0, eupper=0):

        self.lower = lower
        self.upper = upper

        self.value = RandomInt(lower, upper, elower, eupper)
        self.sign = self.sign = "positive" if self.value > 0 else "negative"
        if self.value > 0:
            self.ord = self.ordValue()

    def ordValue(self):

        if self.value // 10 % 10 != 1:
            if self.value % 10 == 1:
                suffix = "st"
            elif self.value % 10 == 2:
                suffix = "nd"
            elif self.value % 10 == 3:
                suffix = "rd"
            else:
                suffix = "th"
        else:
            suffix = "th"

        return str(self.value)+suffix


class RANDFLOAT:

    __slots__ = "lower", "upper", "precision", "value"
    def __init__(self, lower, upper, precision=3):

        self.lower = lower
        self.upper = upper
        self.precision = precision

        self.value = RandomFloat(self.lower, self.upper, self.precision)





class FRACTION:

    def __init__(self, valLower, valUpper, numLower, numUpper):

        self.valLower = valLower
        self.valUpper = valUpper
        self.numLower = numLower
        self.numUpper = numUpper

        self.numerator, self.denominator, self.value = RandFraction(self.valLower, self.valUpper, self.numLower, self.numUpper)

class AS:

    def __init__(self, a1, a2, d1, d2):
        self.first = RandomInt(a1, a2)
        self.diff = RandomInt(d1, d2)
        self.sign = "positive" if self.diff > 0 else "negative"
        self.inequality = "greatest" if self.diff > 0 else "least"
        self.limit = "less than" if self.diff > 0 else "greater than"

    def valueByNo(self, args):
        num = int(args)
        return self.first + (num - 1) * self.diff

    def sumByNo(self, args):
        num = int(args)
        return int(num/2 * (self.first + self.valueByNo(num)))

    def product(self, lower, upper):
        pro = 1
        for n in range(int(lower), int(upper) + 1):
            pro *= self.valueByNo(n)
        return pro


class MULTIAS(AS):

    def __init__(self, lower, upper):
        super().__init__(10, 20, 30, 40)
        self.base = RandomInt(int(lower), int(upper))
        self.first = 0
        self.diff = self.base
        self.sign = "positive" if self.diff > 0 else "negative"


class GS:

    def __init__(self, gsType = None, spec = None):

        if spec:
            num = 2
        else:
            if gsType:
                if gsType.lower() == "int":
                    num = 0
                elif gsType.lower() == "dec":
                    num = 1
                else:
                    num = random.randint(0, 1)
            else:
                num = random.randint(0, 1)

        if num == 0:
            r = RandomInt(-5, 5, -1, 1)
            a = Decimal(RandomInt(-15, 15)) / Decimal((r ** RandomInt(1, 4)))

        elif num == 1:
            run = True
            while run:
                n, d, v = RandFraction(-1, 1, 2, 7)
                r = Decimal(n) / Decimal(d)
                if r != Decimal(1) and r != Decimal(-1):
                    run = False

            a = Decimal(RandomInt(-5, 5)) / Decimal((r ** RandomInt(1, 4)))

        else:
            a = Decimal(spec[0])
            r = Decimal(spec[1])


        self.first = a
        self.ratio = r
        self.sign = "positive" if self.ratio > 0 else "negative"

    def valueByNo(self, n):
        n = Decimal(n)
        return self.first * (self.ratio ** (n - 1))

    def sumByNo(self, n):

        if n == "inf":
            return self.first / (1 - self.ratio)
        else:
            n = Decimal(n)
            return self.first * (self.ratio ** n - 1)/(self.ratio - 1)

    def sumOdd(self, n):

        newObj = GS(spec=(self.first, self.ratio ** 2))
        return newObj.sumByNo(n)




class POLYNOMIAL:

    def __init__(self, deg, leadingCoeff = 0, fractionSpec = (-2, 2, 5, -5), intSpec = (-7, 7), genMode = None, roots = None):

        self.roots = []
        self.numerator = []
        self.denominator = []
        self.deg = deg

        if not fractionSpec:
            fractionSpec = (-2, 2, 5, -5)

        if not intSpec:
            intSpec = (-7, 7)

        if roots:
            try:
                self.roots = [Fraction(root) for root in roots]
            except:
                self.roots = (roots, )
            for i in self.roots:
                self.denominator.append(i.denominator)
                self.numerator.append(i.numerator)
        else:
            if genMode:
                if genMode == "int":
                    intProb = 1
                elif genMode == "frac":
                    intProb = 0
                else:
                    intProb = 0.5
            else:
                intProb = 0.5

            for i in range(deg):

                if random.random() > intProb:
                    num = 1
                else:
                    num = 0

                if num == 1:
                    n, d, v = RandFraction(*fractionSpec)
                    self.roots.append(v)
                    self.numerator.append(n)
                    self.denominator.append(d)
                elif num == 0:
                    v = RandomInt(*intSpec)
                    self.roots.append(v)
                    self.numerator.append(v)
                    self.denominator.append(1)
                else:
                    raise RangeError("Implementation Error.")

        self.ansRoots = [FractionRepresentation(root.numerator, root.denominator) for root in self.roots]
        newList = [1]

        for i in range(deg):
            oldList = newList
            newList = []
            coeffMax = i + 1
            newRoot = self.roots[i]
            for j in range(0, coeffMax+1):
                if j == 0:
                    newList.append(-1 * newRoot * oldList[j])
                elif j == coeffMax:
                    newList.append(oldList[j - 1])
                else:
                    newList.append(-1 * newRoot * oldList[j] + oldList[j - 1])

        self.coeffList = newList
        if leadingCoeff:
            self.leadingCoeff = leadingCoeff
        else:
            self.leadingCoeff = 1
            for i in self.denominator:
                self.leadingCoeff *= i
        self.displayCoeffList = [Fraction((self.leadingCoeff * coeff)).limit_denominator() for coeff in self.coeffList]


    def coeff(self, n):
        n = int(n)
        return self.coeffList[n]

    def displayCoeff(self, n):
        n = int(n)
        return self.displayCoeffList[n]

    def value(self, x):
        sum = 0
        try:
            x = Decimal(float(x))
        except:
            x = Decimal(float(eval(x)))
        for n in range(self.deg + 1):
            sum += Decimal(float(self.displayCoeffList[n])) * (x ** n)
        return Fraction(sum).limit_denominator()

    def root(self, n):
        n = int(n)
        return self.ansRoots[n]

    def denon(self, n):
        n = int(n)
        return self.denominator[n]

    def numer(self, n):
        n = int(n)
        return self.numerator[n]


class QUADRATIC(POLYNOMIAL):

    def __init__(self, leadingCoeff = 0, genMode = None, fractionSpec = (-2, 2, -5, 5), intSpec = (-7, 7), roots = None):

        super().__init__(2, leadingCoeff, fractionSpec, intSpec, genMode, roots)
        self.rootSum = self.coeffList[1]
        self.rootProduct = self.coeffList[0]
        self.symmetryAxis = - self.displayCoeffList[1]/2/self.displayCoeffList[2]
        self.vertex = self.displayCoeffList[0] - (self.displayCoeffList[1] ** 2/4/self.displayCoeffList[2])
        self.discriminant = (self.displayCoeffList[1]) ** 2 - 4 * self.displayCoeffList[0] * self.displayCoeffList[2]
        self.limit = "maximum" if self.displayCoeffList[2] < 0 else "minimum"


if __name__ == '__main__':

    k = ARRAY("randint", 4, (0, 3))
    for i in range(4):
        print(k.array[i].value)





