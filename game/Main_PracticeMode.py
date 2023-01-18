"""
Main_PracticeMode.py
"""


import pyText
import pyInput
import pyMenu
import mQuestionRead
import mQuestions
import pygame
from pygame.locals import *
import GlobalVar

def m_PracticeMode(screen):

    menu = pyMenu.FrameMenu(screen)

    menu.InsertInput("Difficulty (1-3): ", Text=True, inputColor = (255, 0, 0))

    run = True
    while run:

        confirmed = menu.Typing()
        if confirmed:
            try:
                diff = int(menu.Text())
                if 1 <= diff <= 3:
                    run = False
            except:
                pass

        screen.fill((255, 255, 255))
        menu.Blit()
        GlobalVar.LoopBundle()

    # Stage 2 : Display question and ask for answer
    questionObj = mQuestions.QuestionGenerator(diff, GlobalVar.QuestionDatabase)
    question = questionObj["question"]
    answer = questionObj["answer"]
    time = questionObj["time"]
    diffPt = questionObj["diffPt"]


    menu = pyMenu.FrameMenu(screen)
    menu.InsertText("Difficulty (1-3):    " + str(diff), Text=True)
    menu.InsertText("", Enter=True)
    menu.InsertText("Question:", Subheader=True)
    menu.InsertText(f"Time Limit: {str(time):10}"
                            + f"Difficulty Variation: {str(diffPt):10}", Explanation=True)

    menu.TextWrap(question, Text=True)

    menu.InsertInput("Input your answer: ", inputColor=(255,0,0), Text=True)

    run = True
    while run:


        confirmed = menu.Typing()
        if confirmed:
            ans = menu.Text()
            run = False

        screen.fill((255, 255, 255))
        menu.Blit()
        GlobalVar.LoopBundle()

    correct = mQuestions.AnswerChecker(answer, ans)

    # Stage 3: Displaying results and asking if the player wants to play again

    menu = pyMenu.FrameMenu(screen)
    menu.InsertText("Difficulty (1-3):    " + str(diff), Text=True)
    menu.InsertText("", Enter=True)
    menu.InsertText("Question:", Subheader=True)
    menu.InsertText(f"Time Limit: {str(time):10}"
                            + f"Difficulty Variation: {str(diffPt):10}", Explanation=True)

    menu.TextWrap(question, Text=True)

    menu.InsertText("Input your answer:    " + ans, Text=True)
    menu.InsertText(("You are correct!" if correct else "You are incorrect!") + " Correct answer: " + str(answer), Text=True)

    menu.InsertText("", Enter=True)
    menu.InsertText("Would you like to play again?", Subheader=True)
    menu.InitiateMenu()
    ya = menu.InsertMenu("Yes")
    nah = menu.InsertMenu("Nah")

    run = True
    while run:

        for event in pygame.event.get():
            GlobalVar.Quit(event)
            ha = menu.Scrolling(event)
            if ha == ya:
                m_PracticeMode(screen)
                return
            elif ha == nah:
                return

        screen.fill((255, 255, 255))
        menu.Blit()
        GlobalVar.LoopBundle()



if __name__ == '__main__':
    m_PracticeMode(pygame.display.set_mode((1280, 800)))