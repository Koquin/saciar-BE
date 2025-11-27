from pydantic import BaseModel 
from datetime import datetime 
class CreateClienteDto (BaseModel ):
    nome :str 
    telefone :str 
    pontos :int 
    troco :float =0.0 

class GetClientesDto (BaseModel ):
    nome :str 
    telefone :str 
    pontos :int 
    troco :float 

class UpdateClienteDto (BaseModel ):
    nome :str |None =None 
    telefone :str |None =None 
    pontos :int |None =None 
    troco :float |None =None 

class GetClienteByPhoneDto (BaseModel ):
    telefone :str 

class UsePointsDto (BaseModel ):
    cliente_id :str 
    points :int