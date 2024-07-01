class BaseItemsServiceException(Exception): ...


class UpdateItemError(BaseItemsServiceException):
    def __init__(self, message: str):
        super().__init__(message)


class DeleteItemError(BaseItemsServiceException):
    def __init__(self, message: str):
        super().__init__(message)
