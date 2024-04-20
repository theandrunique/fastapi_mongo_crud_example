from fastapi import HTTPException


class ItemNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Item not found",
        )
