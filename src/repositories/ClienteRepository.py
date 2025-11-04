from pymongo import MongoClient
from models.Cliente import Cliente
from typing import Optional
import re
from bson import ObjectId
from bson.errors import InvalidId

class ClienteRepository:
    def __init__(self, db_name: str, db_url: str):
        print(f'Initiating ClientRepository, variables: \ndb_url: {db_url}, db_name: {db_name}')
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db['clientes']

    def create_cliente(self, cliente: Cliente):
        print(f'In ClienteRepository, method: create_cliente, variables: \ncliente: {vars(cliente)}')

        cliente_dict = cliente.__dict__.copy()
        if cliente_dict.get("id") is None:
            cliente_dict.pop("id")
        result = self.collection.insert_one(cliente_dict)
        cliente_dict["_id"] = str(result.inserted_id)
        return cliente_dict
    
    def get_cliente_by_id(self, cliente_id: str) -> Optional[Cliente]:
            print(f'In ClienteRepository, method: get_cliente_by_id, variables: \ncliente_id: {cliente_id}')
            try:
                object_id = ObjectId(cliente_id)
                data = self.collection.find_one({"_id": object_id})
                if data:
                    if '_id' in data:
                        data['id'] = str(data.pop('_id'))
                    return Cliente(**data) 
                return None   
            except InvalidId:
                print(f"Erro: ID de cliente inválido (formato incorreto): {cliente_id}")
                return None
            except Exception as e:
                print(f"Erro ao buscar cliente por ID: {e}")
                return None

    def get_all_clientes(self) -> list[Cliente]:
        print(f'In ClienteRepository, method: get_all_clientes')
        clientes = []
        for data in self.collection.find():
            data["id"] = str(data["_id"])
            del data["_id"]
            clientes.append(Cliente(**data))
            print(f'Cliente found: {data}')
        return clientes

    def update_cliente(self, cliente_id: str, updated_data: dict) -> bool:
            print(f'In ClienteRepository, method: update_cliente, variables: \ncliente_id: {cliente_id}, updated_data: {updated_data}')
            
            try:
                object_id = ObjectId(cliente_id)
                
                result = self.collection.update_one(
                    {"_id": object_id},
                    {"$set": updated_data}
                )
                return result.acknowledged
                
            except InvalidId:
                print(f"Erro: ID de cliente inválido (formato incorreto): {cliente_id}")
                return False
            except Exception as e:
                print(f"Erro ao tentar atualizar cliente: {e}")
                return False
            
    def delete_cliente(self, cliente_id: str) -> bool:
            print(f'In ClienteRepository, method: delete_cliente, variables: \ncliente_id: {cliente_id}')
            
            try:
                object_id = ObjectId(cliente_id)
                
                result = self.collection.delete_one({"_id": object_id})
                
                if result.deleted_count == 0:
                    print(f'No cliente found with id: {cliente_id} to delete.')
                
                return result.acknowledged
                
            except InvalidId:
                print(f"Erro: ID de cliente inválido (formato incorreto): {cliente_id}")
                return False
            except Exception as e:
                print(f"Erro ao tentar deletar cliente: {e}")
                return False
            
    def get_cliente_by_cpf(self, cpf: str) -> Optional[Cliente]:
        print(f'In ClienteRepository, method: get_cliente_by_cpf, variables: \ncpf: {cpf}')
        data = self.collection.find_one({"cpf": cpf})
        if data:
            data["id"] = str(data.pop("_id"))
            return Cliente(**data)
        return None
    
    def search_clients(self, query: str):
        print(f'In ClienteRepository, method: search_clients, variables: \nquery: {query}')
        clientes = []
        regex = re.compile(f'.*{re.escape(query)}.*', re.IGNORECASE)
        for data in self.collection.find({
            "$or": [
                {"nome": {"$regex": regex}},
                {"cpf": {"$regex": regex}},
                {"telefone": {"$regex": regex}}
            ]
        }):
            data["id"] = str(data["_id"])
            del data["_id"]
            clientes.append(Cliente(**data))
        return clientes