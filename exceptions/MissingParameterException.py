from email import message

from .ExceptionBase import ExceptionBase


class MissingParameterException(ExceptionBase):
    def __init__(self, args_required):
        message = f"{args_required} is required"
        super().__init__(message, status_code=400)
