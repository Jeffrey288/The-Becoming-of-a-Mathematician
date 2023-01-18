
from mQuestionRead import *
from mQuestions import *

def main():

    def DisplayDictList(d):
        for i in d.keys():
            print(str(i) + ' : ', end="")
            print(d[i])

    # WriteQuestion("TestQuestions.txt")
    questionDict = ReadQuestion("TestQuestions.txt")

    """    DisplayDictList(q)
    print()
    print(QuestionFiller(q["obj"], q["questionStm"], q["answerStm"]))"""

    # print(QuestionFiller(q["obj"], q["questionStm"], q["answerStm"]))
    for i in range(100):
        question = QuestionGenerator(2, questionDict)
        print(question["question"], end="              ")
        print(question["answer"])
    ans = input()
    print(AnswerChecker(question["answer"], ans))

    """    MODE1 = "Checkmode"
        MODE2 = "AnswerMode"

        MODE = MODE1

        if MODE == MODE1:
            for i in range(100):
                question = QuestionGenerator(2, questionDict)
                if question["question"] != "":
                    print(question["question"])
                    print(question["answer"])
                print()
        else:
            for i in range(3):
                question = QuestionGenerator(2, questionDict)
                print(question["question"])
                print("Time limit:", question["time"])
                userinput = input("Answer: ")
                print("Correct!" if AnswerChecker(question["answer"], userinput) else "Incorrect!", "The answer is:", end=' ')
                print(question["answer"])
                print()"""


if __name__ == "__main__":
    main()