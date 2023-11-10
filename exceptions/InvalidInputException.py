from .ExceptionBase import ExceptionBase


class InvalidInputException(ExceptionBase):
    def __init__(self, args_required):
        message = f"{args_required} is invalid"
        super().__init__(message, status_code=400)
