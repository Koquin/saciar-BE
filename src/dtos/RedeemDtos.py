from pydantic import BaseModel 
from datetime import datetime 

class CreateRedeemDto (BaseModel ):
    telefone :str 
    pontos :int 

class GetRedeemDto (BaseModel ):
    id :str 
    cliente_id :str 
    telefone :str |None =None
    cliente_nome :str |None =None
    premio :str 
    pontos :int 
    created_at :str 

class UpdateRedeemDto (BaseModel ):
    premio :str |None =None 
    pontos :int |None =None 
