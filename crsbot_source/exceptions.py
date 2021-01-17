class TooManyRequestsError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "Too many requests"
