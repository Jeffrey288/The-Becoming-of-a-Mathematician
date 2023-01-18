"""
mQuestions.py
"""


'''
Question Formats: Dictionary
diff : Difficulty of question
diffpt : Difficulty variation
time : answer time
coeffNo : no of coefficients <- Probably not
coeffOpt : options for coefficients <- Keep?
answer : string
question : string
'''

import re
import random
from math import *
from mQuestionRead import * # for testing in main()
from mQuestionObjects import *
import mDebug
import mQuestionErrors

randIntList = [i for i in range(-7, 0)] + [i for i in range(1, 8)] + [FracValue(-2, 2, -5, 5) for i in range(7)]
randList = list(
    set([i for i in range(-7, 0)] + [i for i in range(1, 8)] + [FracValue(-2, 2, -5, 5) for i in range(7)]))
random.shuffle(randIntList)
random.shuffle(randList)


def Redefine():

    global randIntList
    global randList
    randIntList = [i for i in range(-7, 0)] + [i for i in range(1, 8)] + [Fraction(FracValue(-2, 2, -5, 5)).limit_denominator() for i in range(7)]
    randList = list(
        set([i for i in range(-7, 0)] + [i for i in range(1, 8)] + [Fraction(FracValue(-2, 2, -5, 5)).limit_denominator()  for i in range(7)]))


def Shuffle():

    random.shuffle(randIntList)
    random.shuffle(randList)
    Redefine()
    random.shuffle(randIntList)
    random.shuffle(randList)


class Ques:

    def __init__(self):
        self.last2 = None
        self.last = None


Q = Ques()


def QuestionGenerator(diff, questionDict, index = -1):

    for i in range(5):
        try:

            run = True
            while run:
                questionObj = QuestionFetch(diff, questionDict, index)
                if questionObj["comment"] not in [Q.last, Q.last2]:
                    run = False
                    Q.last = Q.last2
                    Q.last2 = questionObj["comment"]

            comment = questionObj["comment"]
            diffPt = questionObj["diffPt"]
            time = questionObj["time"]
            questionStm = questionObj["questionStm"]
            answerStm = questionObj["answerStm"]
            obj = questionObj["obj"]

            question, answer = QuestionFiller(obj, questionStm, answerStm)
            return {
                "comment": comment,
                "diffPt": diffPt,
                "time": time,
                "question": question,
                "answer": answer
            }
        except Exception as e:
            print("Exception: ", e)
            try:
                print("Problem: \"", comment, "\"")
            except:
                pass

    raise mQuestionErrors.Error("Problem occured in " + "Problem: \"" + comment + "\"")


def QuestionFetch(diff, questionDict, index = -1):

    try:
        if index != -1:
            return questionDict[diff][int(index)]
        else:
            if diff == 7:
                fetchDiff = random.randint(1, 6)
            elif diff in [1, 2, 3]:
                fetchDiff = diff if random.random() > 0.2 else (diff + 2) % 6 + 1
            elif diff in [4, 5, 6]:
                if diff == 4:
                    newDiff = 4
                elif diff == 5:
                    newDiff = 4 if random.random() > 0.7 else 5
                elif diff == 6:
                    newDiff = 5 if random.random() > 0.7 else 6
                fetchDiff = newDiff if random.random() > 0.6 else (newDiff + 2) % 6 + 1
        return questionDict[fetchDiff][random.randint(0, len(questionDict[fetchDiff]) - 1)]
    except:
        raise Exception

"""from memory_profiler import profile
@profile"""
def AnswerChecker(answer, userinput):


    try:
        ans = float(answer)
    except:
        try:
            ans = eval(answer) if isinstance(answer, str) else answer
        except Exception as e:
            mDebug.RaiseError(e)
            # Text answer
            try:
                if answer == userinput:
                    result = True
                else:
                    result = False
            except:
                result = False

        else:
            # Evaluable answers (e.g. fractions)
            try:
                if type(ans) in [type(list([])), type(tuple([])), type(set([]))]:
                    check = set([eval(ansn) if isinstance(ansn, str) else ansn for ansn in ans])
                    if len(check) == 1:
                        check = list(check)[0]
                        him = eval(userinput) if isinstance(userinput, str) else userinput
                        if type(him) in [type(list([])), type(tuple([])), type(set([]))]:
                            him = list(him)[0]
                    else:
                        him = set(eval(userinput)) if isinstance(userinput, str) else set(userinput)
                    if him == check:
                        result = True
                    else:
                        result = False
                elif ans == (eval(userinput) if isinstance(userinput, str) else userinput):
                    result = True
                else:
                    result = False
            except Exception as e:
                result = False

    else:

        if int(ans) == ans:
            # Integral answers
            try:
                if int(ans) == int(eval(userinput)):
                    result = True
                else:
                    result = False
            except:
                result = False

        else:
            # Decimal answers:

            PERCENTAGEERROR = 0.5 / 100

            try:
                if abs((float(eval(userinput)) - ans) / ans) < PERCENTAGEERROR:
                    result = True
                else:
                    result = False
            except:
                result = False



    return result


def GenerateObjects(obj):

    objDict = {}

    for objName in obj.keys():

        item = obj[objName]
        objType = item["objname"].lower()
        args = item["args"].strip()

        OBJ = eval(switch[objType] + args)

        objDict[objName] = OBJ

    return objDict


def Process(objDict, string, count = 0):

    # objDict stores the objects
    # string stores the string to be processed
    # counter stores the recursion depth

    # If there are curly brackets in the string,
    # it is either the whole question or answer statmenet
    # or that it is a placeholder where there are nested placeholders that needs
    # to be evaluated
    if "{" in string or "}" in string:

        tempString = ""
        returnString = ""
        counter = 0
        inEnv = False

        # Reading the string from left to right, ...
        for character in string:

            # print(str(counter)+str(character), end=" ")

            # We enter an environment when we meet a base bracket
            # Start the environment, and write the characters to another stream, called tempString
            # If the curly bracket is not a base bracket
            # We drop the curly brackets
            # Otherwise, we include the curly brackets
            # Increasing the number of corresponding close brackets by 1
            if character == "{":

                if counter == 0:
                    pass
                else:
                    tempString += character
                counter += 1
                inEnv = True

            # When we meet a closing bracket
            # We reduce the required closing brackets by 1
            # If the closing bracket is a base bracket, and we are inside the environment
            # We leave the environment
            # We send the tempString to another Process, which will retrieve the attribute
            # and append it to the returnString
            # if there are no nesting brackets
            # The program will continue writing characters to tempString if the
            # environment is not ended
            elif character == "}":

                counter -= 1

                if counter == 0 and inEnv:

                    inEnv = False
                    # print("\n" + tempString)

                    tempString = str(Process(objDict, tempString, count + 1))
                    # print(tempString)
                    returnString += tempString

                    tempString = ""

                if counter > 0:

                    tempString += character

            # for characters that are not curly brackets
            # we write them to tempString if we're in the enviroment
            # and to the return string if not
            else:
                if inEnv:
                    tempString += character
                else:
                    returnString += character

            # print(str(counter) + character, end=" ")

        # if the recursion depth is greater than 1,
        # then it is a placeholder with nested placeholders
        # in this case, we evaluate the placeholder
        # and include the displayOptions.
        inString = returnString
        if count > 0:
            returnString = str(AttrRetriever(objDict, returnString))
        if count == 1:
            returnString = DisplayOptions(inString, returnString)

        return returnString

    # If there are no curly brackets in the string...
    else:

        # If the recursion depth is 1 (contains display options)
        # retrieve the attributes,
        # and apply the display options
        if count == 1:
            inString = string
            returnString = str(AttrRetriever(objDict, string))
            returnString = DisplayOptions(inString, returnString)

        # If the recursion depth is greater than 1
        # just retrieves the attributes
        elif count > 1:
            returnString = str(AttrRetriever(objDict, string))

        # If for some reason, the recursion depth is 0
        # just return the string
        else:
            returnString = string

        return returnString


def DisplayOptions(inString, returnString):

    if "_hideone" in inString:
        if returnString == "1":
            string = ""
        elif returnString == "-1":
            string = "-"

    if "_showsign" in inString:
        try:
            if float(eval(returnString)) >= 0:
                string = "+" + returnString
        except:
            pass

    if "_showsignspace" in inString:
        try:
            if float(eval(returnString)) > 0:
                string = "+ " + returnString
            else:
                string = "- " + str(abs(eval(returnString)))
        except:
            pass

    try:
        return string
    except:
        return returnString


def QuestionFiller(obj, questionStm, answerStm):


    question = questionStm
    answer = answerStm
    failNo = 0


    while True:
        try:

            Shuffle()
            objCopy = obj.copy()
            objDict = GenerateObjects(objCopy)
            question = Process(objDict, question)
            answer = Process(objDict, answer)
            try:
                if "/" not in answer:
                    answer = eval(answer)
            except:
                pass

        except Exception as exception:
            del objDict
            del question
            del answer
            question = questionStm
            answer = answerStm
            failNo += 1
            if failNo >= 1000:
                raise exception
        else:
            break

    # Postprocessing
    answer = PostProcessing(answer)

    return question, answer


def AttrRetriever(objDict, argsString):

    specList = re.split(",", argsString)

    obj = objDict[specList[0]]
    argsList = specList[1:]

    sysArgs = 0
    tempArgs = []
    for args in argsList[1:]:
        if "_" not in args:  # if _ is in args, then it specifies a display option
            tempArgs.append(args)
        else:
            sysArgs += 1

    if (len(argsList[1:]) - sysArgs == 0 and sysArgs > 0) or len(argsList) == 1:
        coeff = getattr(obj, argsList[0])
    else:
        coeff = ExecuteFunction(obj, argsList[0], tempArgs)

    return str(coeff)


def PostProcessing(answer):

    try:
        if type(answer) == type(""):
            if "/" in answer:
                a, b = re.split("/", answer)
                if b == "1":
                    newAnswer = a
                else:
                    hcf = HCF(a,b)
                    if hcf != 1:
                        newAnswer = str(a//hcf)+"/"+str(b//hcf)
                    else:
                        newAnswer = answer
            else:
                newAnswer = answer
        else:
            newAnswer = answer
    except:
        newAnswer = answer

    try:
        if isinstance(answer, float):
            newAnswer = f'{answer:.4g}'
        else:
            newAnswer = answer
    except:
        newAnswer = answer

    if isinstance(newAnswer, str):
        if "\uff0c" in newAnswer:
            newAnswer.replace("\uff0c", ",")

    try:
        lst = eval(newAnswer)
        if type(lst) in [type(list([])), type(tuple([])), type(set([]))]:
            newAnswer = list(set(lst))
    except:
        pass

    try:
        if isinstance(answer, Fraction):
            newAnswer = str(answer.numerator) + "/" + str(answer.denominator)
    except:
        pass

    try:
        return newAnswer
    except:
        return answer


def main():

    def DisplayDictList(d):
        for i in d.keys():
            print(str(i) + ' : ', end="")
            print(d[i])

    questionDict = ReadQuestion("files/Questions.json")

    while True:
        question = QuestionGenerator(random.randint(1, 6), questionDict)
        DisplayDictList(question)

    for k in range(6):
        j = 0
        run = True
        while run:
            try:

                # For each question, repeat five times
                for i in range(5):

                    # Generates a question
                    question = QuestionGenerator(k+1, questionDict, j)

                    # Print out the question
                    print(question["comment"] + ": " + question["question"])

                    # Prompt for input
                    ans = input()

                    # Checks the answer and display the results
                    print(AnswerChecker(question["answer"], ans), question["answer"])

                    print()
                j += 1
            except:
                run = False


if __name__ == "__main__":
    main()