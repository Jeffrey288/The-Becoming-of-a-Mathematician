"""
mQuestionWorkplace.py
"""


from mQuestions import *


def main():

    def DisplayDictList(d):
        for i in d.keys():
            print(str(i) + ' : ', end="")
            print(d[i])

    questionDict = ReadQuestion("files/TestQuestions.json")

    answer = "3/2"
    ans = 3/2
    print(AnswerChecker(answer, ans), answer)

    q = QuestionFetch(6, questionDict, 0)
    print()
    print(QuestionFiller(q["obj"], q["questionStm"], q["answerStm"]))

    """for k in range(6):
        while True:
            try:
                question = QuestionGenerator(k+1, questionDict, 0)
                print(question["comment"] + ": " + question["question"])
                ans = input()
                print(AnswerChecker(question["answer"], ans), question["answer"])
                print()
            except Exception as e:
                print (e)
                break"""

    for k in range(6):
        j = 0
        run = True
        while run:
            try:
                for i in range(5):
                    question = QuestionGenerator(6, questionDict, j)
                    print(question["comment"] + ": " + question["question"])
                    ans = input()
                    print(AnswerChecker(question["answer"], ans), question["answer"])
                    print()
                j += 1
            except Exception as e:
                run = False

main()