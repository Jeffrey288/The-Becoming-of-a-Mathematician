"""
ASequence.py
"""

from ATextBox import *
import pyAnimation
import GlobalVar

def Epilogue(screen):

    GlobalVar.audio.FeedAudio(GlobalVar.AmbientMusic)

    scene = Scene(screen, nowHeight = 0.25)

    def Zero():
        scene.TextBox.InsertText("~ Epilogue ~", "center", True)

    def One():
        scene.TextBox.InsertText("You have defeated the greatest Mathematicians in all of history.", "center")

    def Two():
        scene.TextBox.InsertText("And so, you are recognized as the most influential Mathematician in the whole world.", "center")

    def Three():
        scene.TextBox.InsertText("You have reached the paramount of human intelligence.", "center")

    def Four():
        scene.TextBox.InsertText("However, as Einstein has said:", "center")
        scene.TextBox.InsertText("Intellectual growth should commence at birth and cease only at death.", "center", True)

    def Five():
        scene.TextBox.InsertText("Do not be satisfied just because you have become the best.", "center")

    def Six():
        scene.TextBox.InsertText("Strive for excellence and perfection, and open new roads that no one have ever found before.", "center")

    def Seven():
        scene.TextBox.InsertText("I believe you can do it.", "center")

    def Eight():
        scene.TextBox.InsertText("Thank you for playing my game, The Becoming of the Mathematician.", "center")

    def Nine():
        scene.TextBox.InsertText("You may return to the village, save your game, and continue levelling yourself until you reach the topmost level. You can also quit the game without saving.")


    FunctionList = [
        Zero,
        One,
        Two,
        Three,
        Four,
        Five,
        Six,
        Seven,
        Eight,
        Nine
    ]

    GraphicsList = [
        "0", "0", "1", "2", "3", "4", "5", "6", "7", "7"
    ]

    scene.ChangeWallpaper("assets/EndingImage/Scene" + "0" + ".jpg", False)
    def displayFunction():
        scene.Update()
        scene.Display()

    pyAnimation.EnterFade(screen, displayFunction, GlobalVar.CentralClock, GlobalVar.GameFPS)
    for num, func in enumerate(FunctionList):

        scene.TextBox.Reset()
        func()
        scene.TextBox.Finalize()

        scene.ChangeWallpaper("assets/EndingImage/Scene" + GraphicsList[num] + ".jpg")

        run = True
        while run:

            for event in pygame.event.get():
                GlobalVar.Quit(event)
                result = scene.TextBox.Event(event)
                if result:
                    run = False
                    break

            scene.Display()
            LoopBundle()

    ret = 0
    qui = 1

    def Back():
        scene.TextBox.Reset()
        scene.TextBox.InsertMenu("Return to the Village")
        scene.TextBox.InsertMenu("Quit Game")
        scene.TextBox.Finalize()

    def Confirm():
        scene.TextBox.Reset()
        scene.TextBox.InsertText("Are you sure?", bold=True)
        nah = scene.TextBox.InsertMenu("No")
        ya = scene.TextBox.InsertMenu("Yes")
        scene.TextBox.Finalize()

        run = True
        while run:

            for event in pygame.event.get():
                GlobalVar.Quit(event)
                result = scene.TextBox.Event(event)
                if result == nah:
                    return False
                elif result == ya:
                    return True

            scene.Display()
            LoopBundle()

    Back()

    run = True
    while run:

        for event in pygame.event.get():
            GlobalVar.Quit(event)
            result = scene.TextBox.Event(event)
            if result == ret:
                return False
            elif result == qui:
                if Confirm():
                    return True
                else:
                    Back()

        scene.Display()
        LoopBundle()


def AdventureModeSequence(screen):

    GlobalVar.audio.FeedAudio(GlobalVar.AmbientMusic)

    scene = Scene(screen, nowHeight = 0.25)

    def Zero():
        scene.TextBox.InsertText("~ The Becoming of a Mathematician ~", "center", True)

    def One():
        scene.TextBox.InsertText("The story takes place in this small, remote village.")
        scene.TextBox.InsertText("Far away from the hustling cities, it was a quiet village.")

    def Two():
        scene.TextBox.InsertText("Then, you were born into this world, just like any other child.")

    def Three():
        scene.TextBox.InsertText("In this remote village, you played around in the fields all day.")
        scene.TextBox.InsertText("Sometimes, you helped your parents with farming.")

    def Four():
        scene.TextBox.InsertText("On one special occasion, you parents brought you out to town.")
        scene.TextBox.InsertText("It was your first time, so you were very excited.")

    def Five():
        scene.TextBox.InsertText("You wandered around this mysterious city, and found a rather modern looking shop.")
        scene.TextBox.InsertText("Out of curiosity, you entered this shop.")

    def Six():
        scene.TextBox.InsertText("You walked around the shop, which was lined up with bookshelves of books, and you randomly pulled a book off the shelf.")
        scene.TextBox.InsertText("What you found was a book filled with eccentric and mysterious symbols. It was a Math book.")

    def Seven():
        scene.TextBox.InsertText("Your desire to learn resonated, and you asked your parents to buy you this book.")
        scene.TextBox.InsertText("As you learned and learned, you came across the works of famous Mathematicians, and your admiration grew along with the passion to meet them.")

    def Eight():
        scene.TextBox.InsertText("And you finally set your eyes on a final goal: defeat these Mathematicians and claim the position of being the best Mathematician.")
        scene.TextBox.InsertText("Just like so, you embarked on a journey to travel around the world to defeat these Mathematicians.")

    FunctionList = [
        Zero,
        One,
        Two,
        Three,
        Four,
        Five,
        Six,
        Seven,
        Eight
    ]

    def displayFunction():
        screen.fill((0, 0, 0))
        scene.Display()

    pyAnimation.EnterFade(screen, displayFunction, GlobalVar.CentralClock, GlobalVar.GameFPS)
    for num, func in enumerate(FunctionList):

        scene.TextBox.Reset()
        func()
        scene.TextBox.Finalize()

        scene.ChangeWallpaper("assets/StoryImage/Scene" + str(num) + ".jpg")

        run = True
        while run:

            for event in pygame.event.get():
                GlobalVar.Quit(event)
                result = scene.TextBox.Event(event)
                if result:
                    run = False
                    break

            scene.Display()
            LoopBundle()



if __name__ == '__main__':
    s = pygame.display.set_mode((1200, 800))
    Epilogue(s)
    AdventureModeSequence(s)