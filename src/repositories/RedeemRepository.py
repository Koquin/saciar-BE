from pymongo import MongoClient
from ..models.Redeem import Redeem
from typing import Optional 
import re 
from bson import ObjectId 
from bson .errors import InvalidId 

class RedeemRepository :
    def __init__ (self ,db_name :str ,db_url :str ):
        print (f'Initiating RedeemRepository, variables: \ndb_url: {db_url }, db_name: {db_name }')
        self .client =MongoClient (db_url )
        self .db =self .client [db_name ]
        self .collection =self .db ['redeems']

    def create_redeem (self ,redeem :Redeem ):
        print (f'In RedeemRepository, method: create_redeem, variables: \nredeem: {vars (redeem )}')

        redeem_dict =redeem .__dict__ .copy ()
        if redeem_dict .get ("id")is None :
            redeem_dict .pop ("id")
        result =self .collection .insert_one (redeem_dict )
        redeem_dict ["_id"]=str (result .inserted_id )
        return redeem_dict 

    def get_redeem_by_id (self ,redeem_id :str )->Optional [Redeem ]:
            print (f'In RedeemRepository, method: get_redeem_by_id, variables: \nredeem_id: {redeem_id }')
            try :
                object_id =ObjectId (redeem_id )
                data =self .collection .find_one ({"_id":object_id })
                if data :
                    if '_id'in data :
                        data ['id']=str (data .pop ('_id'))
                    return Redeem (**data )
                return None 
            except InvalidId :
                print (f"Erro: ID de redeem inválido (formato incorreto): {redeem_id }")
                return None 
            except Exception as e :
                print (f"Erro ao buscar redeem por ID: {e }")
                return None 

    def get_all_redeems (self )->list [Redeem ]:
        print (f'In RedeemRepository, method: get_all_redeems')
        redeems =[]
        for data in self .collection .find ():
            data ["id"]=str (data ["_id"])
            del data ["_id"]
            redeems .append (Redeem (**data ))
            print (f'Redeem found: {data }')
        return redeems 

    def get_redeems_by_cliente_id (self ,cliente_id :str )->list [Redeem ]:
        print (f'In RedeemRepository, method: get_redeems_by_cliente_id, variables: \ncliente_id: {cliente_id }')
        redeems =[]
        for data in self .collection .find ({"cliente_id":cliente_id }):
            data ["id"]=str (data ["_id"])
            del data ["_id"]
            redeems .append (Redeem (**data ))
        return redeems 

    def update_redeem (self ,redeem_id :str ,updated_data :dict )->bool :
            print (f'In RedeemRepository, method: update_redeem, variables: \nredeem_id: {redeem_id }, updated_data: {updated_data }')

            try :
                object_id =ObjectId (redeem_id )

                result =self .collection .update_one (
                {"_id":object_id },
                {"$set":updated_data }
                )
                return result .acknowledged 

            except InvalidId :
                print (f"Erro: ID de redeem inválido (formato incorreto): {redeem_id }")
                return False 
            except Exception as e :
                print (f"Erro ao tentar atualizar redeem: {e }")
                return False 

    def delete_redeem (self ,redeem_id :str )->bool :
            print (f'In RedeemRepository, method: delete_redeem, variables: \nredeem_id: {redeem_id }')

            try :
                object_id =ObjectId (redeem_id )

                result =self .collection .delete_one ({"_id":object_id })

                if result .deleted_count ==0 :
                    print (f'No redeem found with id: {redeem_id } to delete.')

                return result .acknowledged 

            except InvalidId :
                print (f"Erro: ID de redeem inválido (formato incorreto): {redeem_id }")
                return False 
            except Exception as e :
                print (f"Erro ao tentar deletar redeem: {e }")
                return False 

    def search_redeems (self ,query :str ):
        print (f'In RedeemRepository, method: search_redeems, variables: \nquery: {query }')
        redeems =[]
        regex =re .compile (f'.*{re .escape (query )}.*',re .IGNORECASE )
        for data in self .collection .find ({
        "$or":[
        {"premio":{"$regex":regex }},
        {"cliente_id":{"$regex":regex }},
        {"cliente_nome":{"$regex":regex }},
        {"cliente_telefone":{"$regex":regex }},
        {"created_at":{"$regex":regex }}
        ]
        }):
            data ["id"]=str (data ["_id"])
            del data ["_id"]
            redeems .append (Redeem (**data ))
        return redeems 
