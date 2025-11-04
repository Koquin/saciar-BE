import logging
from exceptions.ClienteConflictException import ClienteConflictException
from models.Cliente import Cliente
from datetime import datetime
from exceptions.NoClientesFoundException import NoClientesFoundException
from exceptions.ClienteNotFoundException import ClienteNotFoundException
from dtos.ClienteDtos import CreateClienteDto
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ClienteService:
    def __init__(self, clienteRepository):
        logger.info(f'Initiating ClienteService, variables: \nclienteRepository: {clienteRepository}')
        self.clienteRepository = clienteRepository
    
    def createCliente(self, CreateClienteDto):
        logger.info(f'In ClienteService, method: createCliente, variables: \ncreateClienteDto: {CreateClienteDto}')
        cliente = self.clienteRepository.get_cliente_by_cpf(CreateClienteDto.cpf)
        if (cliente):
            logger.error('Error finding cliente with this CPF, conflict detected.')
            raise ClienteConflictException()
        
        clienteModel = Cliente(
            id = None,
            cpf=CreateClienteDto.cpf, 
            nome=CreateClienteDto.nome,
            telefone=CreateClienteDto.telefone,
            pontos=CreateClienteDto.pontos,
            qtd_gasta=0,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        response = self.clienteRepository.create_cliente(clienteModel)
        logger.info(f'Cliente created successfully. Response: {response}')
        return response
    
    def getAllClientes(self):
        logger.info(f'In ClienteService, method: getAllClientes')
        clientes = self.clienteRepository.get_all_clientes()
        
        if not clientes:
            logger.warning('No clients found in the database.')
            raise NoClientesFoundException()
        
        clientes_dto = [
            {
                "id": c.id,
                "nome": c.nome,
                "cpf": c.cpf,
                "telefone": c.telefone,
                "pontos": c.pontos
            }
            for c in clientes
        ]
        return clientes_dto

    def search_clients_dto(self, query: str) -> List[CreateClienteDto]:
        clientes = self.clienteRepository.search_clients(query)
        return [CreateClienteDto(nome=c.nome, cpf=c.cpf, telefone=c.telefone, pontos=c.pontos) for c in clientes]
    
    def updateCliente(self, idCliente, updateClienteDto):
            logger.info(f'In ClienteService, method: updateCliente, variables: \nupdateCliente: {updateClienteDto}, idCliente: {idCliente}')
            
            cliente = self.clienteRepository.get_cliente_by_id(idCliente)
            if not cliente:
                logger.error(f'Error finding the cliente with id {idCliente}.')
                raise ClienteNotFoundException()
            
            updatedData = updateClienteDto.model_dump(exclude_none=True)

            updatedData['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            updatedCliente = self.clienteRepository.update_cliente(idCliente, updatedData)
            
            logger.info(f'Cliente with id {idCliente} updated successfully.')
            logger.info(f'\nUpdatedCliente: {updatedCliente}')
            return updatedCliente

    def deleteClienteById(self, idCliente: str):
        logger.info(f'In ClienteService, method: deleteCliente, variables: \nidCliente: {idCliente}')
        cliente =  self.clienteRepository.get_cliente_by_id(idCliente)
        print(cliente)
        if not cliente:
            logger.error(f'Error finding cliente with ID {idCliente} for deletion.')
            raise ClienteNotFoundException()

        deletedCliente =  self.clienteRepository.delete_cliente(cliente.id)
        logger.info(f'Cliente with ID {idCliente} deleted successfully.')
        return deletedCliente