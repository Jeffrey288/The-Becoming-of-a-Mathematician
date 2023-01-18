import pygame.locals
import threading


def DebugThread():

    import pygame

    event = pygame.event.Event(pygame.locals.KEYDOWN, {"key": pygame.locals.K_RETURN})
    print(event.type)
    print(event.key)

    while True:
        pygame.event.post(event)
        print("hai")


thread = threading.Thread(target=DebugThread)
thread.start()