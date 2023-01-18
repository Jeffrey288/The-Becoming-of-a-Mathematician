"""
mErrors.py
"""

class GameError(Exception):
    pass


class QuestionError(GameError):

    def __int__(self):
        self.message = "QUestions.json not found."


class BossError(GameError):

    def __int__(self):
        self.message = "Bosses.txt not found."