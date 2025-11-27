from pydantic import BaseModel 


from pydantic import BaseModel 

class postPurchaseDto (BaseModel ):
    telefone :str 
    valor :float 
    is_delivery :bool 
    isFromClient :bool =False 
    nome :str |None =None 
    date :str |None =None 