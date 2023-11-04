class MovieException(Exception):
    def __init__(self, message, params=None, status=None):
        self.message = message
        self.params = params
        self.status = status

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"
