from .ExceptionBase import ExceptionBase


class UnsupportedChainIdException(ExceptionBase):
    def __init__(self, chain_id, supported_chain_ids):
        message = f"{chain_id} is not a supported chain for this service, chain_id should be one of {supported_chain_ids}"
        super().__init__(message, status_code=400)
