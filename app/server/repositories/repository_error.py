class RepositoryError(BaseException):
    message: str
    code: int
    def __init__(self, message: str, statuscode: int):
        self.message = message
        self.code = statuscode