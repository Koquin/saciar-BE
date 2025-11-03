#why is this error happening?
#TypeError: descriptor '__init__' of 'super' object needs an argument
#How to fix it?
#You need to call super() with parentheses to properly initialize the parent class. Change super.__init__(...) to super().__init__(...). Here is the corrected code:
from fastapi import HTTPException
class ClienteNotFoundException(HTTPException):
    def __init__(self, detail:str = 'Error: Cliente not found'):
        super().__init__(status_code=404, detail=detail)