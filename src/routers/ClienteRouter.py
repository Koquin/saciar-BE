from fastapi import APIRouter
from controllers.ClienteController import ClienteController
from repositories.ClienteRepository import ClienteRepository
from services.ClienteService import ClienteService
from dtos.ClienteDtos import CreateClienteDto
from typing import List
from fastapi import Query
from dtos.ClienteDtos import UpdateClienteDto

db_name = "gerenciamento_clientes"
db_url = "mongodb://localhost:27017/"

clienteRepository = ClienteRepository(db_name, db_url)
clienteService = ClienteService(clienteRepository)
clienteController = ClienteController(clienteService)

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", summary="Create a new cliente", status_code=201)
def postCliente(CreateClienteDto: CreateClienteDto):
    print(f'In ClienteRouter, method: postCliente, variables: \ncreateClienteDto: {CreateClienteDto}')
    response =  clienteController.postCliente(CreateClienteDto)
    return response
    
@router.get("/", summary="Get all clientes", status_code=200)
def getAllClientes():
    print(f'In ClienteRouter, method: getAllClientes')
    response =  clienteController.getAllClientes()
    return response
    
@router.put("/{idCliente}", summary="Update a cliente by ID", status_code=200)
def updateCliente(idCliente, atualizarClienteDto: UpdateClienteDto):
    print(f'In ClienteRouter, method: updateCliente, variables: \nidCliente: {idCliente}, atualizarClienteDto: {atualizarClienteDto}')
    response = clienteController.updateCliente(idCliente, atualizarClienteDto)
    return response
    
@router.delete("/{idCliente}", summary="Delete a cliente by ID", status_code=204)
def deleteCliente(idCliente):
    print(f'In ClienteRouter, method: deleteCliente, variables: \n idCliente: {idCliente}')
    response = clienteController.deleteCliente(idCliente)
    return response

@router.get("/search", response_model=List[CreateClienteDto])
def search_clients(q: str = Query(None, description="Nome, CPF ou telefone para buscar")):
    print(f'In ClienteRouter, method: search_clients, variables: \nquery: {q}')
    return clienteController.search_clients(q)