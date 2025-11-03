from fastapi import HTTPException
class InvalidCredentialsException(HTTPException):
    def __init__(self, detail = "Invalid credentials provided"):
        super().__init__(status_code=401, detail=detail)