from pydantic import BaseModel
from datetime import datetime
class CreateClienteDto(BaseModel):
    nome: str
    cpf: str
    telefone: str
    pontos: int

class GetClientesDto(BaseModel):
    nome: str
    cpf: str
    telefone: str
    pontos: int

class UpdateClienteDto(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    telefone: str | None = None
    pontos: int | None = None

class GetClienteByCpfDto(BaseModel):
    cpf: str

class UsePointsDto(BaseModel):
    cliente_id: str
    points: int