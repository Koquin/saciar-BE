from dtos.ClienteDtos import CreateClienteDto
from typing import List

class ClienteController:
    def __init__(self, clienteService):
        print(f'Initiating ClienteController, variables: \nclienteService: {clienteService}')
        self.clienteService = clienteService

    def postCliente(self, CreateClienteDto):
        print(f'In ClienteController, method: postCliente, variables: \nclienteDto: {CreateClienteDto}')
        response =  self.clienteService.createCliente(CreateClienteDto)
        return response

    def getAllClientes(self):
        print(f'In ClienteController, method: getAllClientes')
        response =  self.clienteService.getAllClientes()
        return response

    def updateCliente(self, idCliente, atualizarClienteDto):
        print(f'In ClienteController, method: updateCliente, variables: \nidCliente: {idCliente}, atualizarClienteDto: {atualizarClienteDto}')
        return self.clienteService.updateCliente(idCliente, atualizarClienteDto)

    def deleteCliente(self, idCliente: str):
        print(f'In ClienteController, method: deleteCliente, variables: \n idCliente: {idCliente}')
        response = self.clienteService.deleteClienteById(idCliente)
        return response
    
    def search_clients(self, query: str) -> List[CreateClienteDto]:
        if not query:
            return self.get_all_clientes()
        return self.clienteService.search_clients_dto(query)
    
    def getClienteByCpf(self, cpf: str):
        print(f'In ClienteController, method: getClienteByCpf, variables: \ncpf: {cpf}')
        cliente = self.clienteService.getClienteByCpf(cpf)
        return cliente