from pydantic import BaseModel
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