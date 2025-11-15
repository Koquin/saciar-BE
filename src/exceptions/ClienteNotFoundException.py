



from fastapi import HTTPException 
class ClienteNotFoundException (HTTPException ):
    def __init__ (self ,detail :str ='Error: Cliente not found'):
        super ().__init__ (status_code =404 ,detail =detail )