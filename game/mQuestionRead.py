"""
mQuestionRead.py
"""

import json
import mErrors


def DisplayDictList(d):
    for i in d.keys():
        print(str(i) + ' : ')
        for num, j in enumerate(d[i]):
            print(f" {str(num)+'.':<4}", end="")
            print(j)


def ObjectJSONGenerator():

    print("Object (input -1 to end):")
    obj = {}
    readObj = True
    while readObj:
        objName = input(f"{'Object Name:':30} ")
        if objName == "-1":
            runObj = False
            break
        objType = input(f"{'Object Type (objname):':30} ")
        args = input(f"{'Arguments (args):':30} ")
        obj[objName] = {
            "objname": objType,
            "args": args
        }

        code = json.dumps(obj)

    return code


def WriteQuestion(filename):

    try:
        questionFile = open(filename, 'r')
        questionList = json.loads(questionFile.read())
    except:
        questionList = []

    run = True
    while run:

        print("Please input a question: (Insert comment = -1 to end)")
        comment = input(f"{'Comment:':30} ")
        if comment == '-1':
            run = False
            break
        diff = int(input(f"{'Difficulty (diff):':30} "))
        diffpt = float(input(f"{'Difficulty Variation (diffpt):':30} "))
        time = int(input(f"{'Answering Time (time):':30} "))

        obj = input(f"{'Object (obj)':30} ")
        questionStm = input(f"{'Question (questionStm):':30} ")
        answerStm = input(f"{'Answer (answerStm):':<30} ")

        questionList.append({
            "comment": comment,
            "diff": diff,
            "diffPt": diffpt,
            "time": time,
            "obj": obj,
            "questionStm": questionStm,
            "answerStm": answerStm
        })

    storeStr = json.dumps(questionList, indent=4)

    questionFile = open(filename, 'w')
    questionFile.write(storeStr)


def ReadQuestion(filename):

    def RemoveKey(dictionary, key):
        r = dict(dictionary)
        del(r[key])
        return r

    try:
        questionFile = open(filename, 'r')
        questionList = json.loads(questionFile.read())
    except Exception as e:
        raise mErrors.QuestionError
    else:
        QuestionDict = {}

        for i in range(1,7):
            QuestionDict[i] = []

        try:
            for q in questionList:
                diff = q["diff"]
                q = RemoveKey(q, "diff")
                q["obj"] = json.loads(q["obj"])
                QuestionDict[diff].append(q)
        except Exception as e:
            print(q["comment"], "an error has occured")
            raise e

        return QuestionDict

