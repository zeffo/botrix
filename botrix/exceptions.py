class BotrixException(Exception):
    def __init__(self, error):
        self.error = error
    def __repr__(self):
        return self.error

class RatelimitException(BotrixException):
    pass