class InvalidBody(Exception):
    def __init__(self, message: str = "Invalid_body"):
        self.message = message
