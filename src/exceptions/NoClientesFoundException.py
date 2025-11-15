from fastapi import HTTPException 
class NoClientesFoundException (HTTPException ):
    def __init__ (self ,detail :str ='Nenhum cliente achado no banco de dados'):
        super ().__init__ (status_code =404 ,detail =detail )
