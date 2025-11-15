from fastapi import HTTPException 

class ClienteConflictException (HTTPException ):
    def __init__ (self ,detail :str ="Usuário já existe!"):
        super ().__init__ (status_code =403 ,detail =detail )
