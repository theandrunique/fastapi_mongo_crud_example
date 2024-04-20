from fastapi import HTTPException


class ItemNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=404,
            detail="Item not found",
        )
