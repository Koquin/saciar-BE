from pymongo import MongoClient 
from bson import ObjectId 
from bson .errors import InvalidId 
from datetime import datetime 

class PurchaseRepository :
    def __init__ (self ,db_name :str ,db_url :str ):
        print (f'Initiating PurchaseRepository, variables: \ndb_url: {db_url }, db_name: {db_name }')
        self .client =MongoClient (db_url )
        self .db =self .client [db_name ]
        self .collection =self .db ['compras']
        self .db_name =db_name 
        self .db_url =db_url 

    def create_purchase (self ,purchase :dict ):
        print (f'In PurchaseRepository, method: create_purchase, variables: \npurchase: {purchase }')
        purchase_dict =purchase .copy ()

        if 'created_at'not in purchase_dict :
            purchase_dict ['created_at']=datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")
        result =self .collection .insert_one (purchase_dict )
        purchase_dict ['_id']=str (result .inserted_id )
        return purchase_dict 

    def get_all_purchases (self )->list :
        print ('In PurchaseRepository, method: get_all_purchases')
        purchases =[]
        for data in self .collection .find ():
            data ['id']=str (data ['_id'])
            del data ['_id']
            purchases .append (data )
        return purchases 

    def search_purchases (self ,query :str )->list :
        print (f'In PurchaseRepository, method: search_purchases, variables: \n query: {query }')
        purchases =[]
        try :

            try :
                valor_query =float (query )
                valor_search ={'valor':valor_query }
            except ValueError :
                valor_search ={}

            regex ={'$regex':query ,'$options':'i'}
            search_conditions =[
            {'cliente':regex },
            {'cpf':regex },
            {'data':regex }
            ]

            if valor_search :
                search_conditions .append (valor_search )

            cursor =self .collection .find ({
            '$or':search_conditions 
            })
            for data in cursor :
                data ['id']=str (data ['_id'])
                del data ['_id']
                purchases .append (data )
        except Exception as e :
            print (f'Erro ao buscar purchases: {e }')
        return purchases 

    def delete_purchase (self ,purchase_id :str )->bool :
        print (f'In PurchaseRepository, method: delete_purchase, variables: \n purchase_id: {purchase_id }')
        try :
            object_id =ObjectId (purchase_id )
            result =self .collection .delete_one ({'_id':object_id })
            if result .deleted_count ==0 :
                print (f'No purchase found with id: {purchase_id } to delete.')
            return result .acknowledged 
        except InvalidId :
            print (f'Erro: ID de purchase inválido (formato incorreto): {purchase_id }')
            return False 
        except Exception as e :
            print (f'Erro ao tentar deletar purchase: {e }')
            return False 
