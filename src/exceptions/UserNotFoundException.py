from fastapi import HTTPException
class UserNotFoundException(HTTPException):
    def __init__(self, detail = "User not found"):
        super().__init__(status_code=404, detail=detail)