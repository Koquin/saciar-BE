import logging 
from datetime import datetime 
from typing import Optional 

from repositories .ClienteRepository import ClienteRepository 

logging .basicConfig (level =logging .INFO ,format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger =logging .getLogger (__name__ )

class PurchaseService :
	def __init__ (self ,purchaseRepository ,clienteRepository :Optional [ClienteRepository ]=None ,db_name :str ="gerenciamento_clientes",db_url :str ="mongodb://localhost:27017/"):
		logger .info (f'Initiating PurchaseService, variables: \npurchaseRepository: {purchaseRepository }, clienteRepository: {clienteRepository }')
		self .purchaseRepository =purchaseRepository 
		if clienteRepository is None :
			self .clienteRepository =ClienteRepository (db_name ,db_url )
		else :
			self .clienteRepository =clienteRepository 

	def createPurchase (self ,postPurchaseDto ):
		logger .info (f'In PurchaseService, method: createPurchase, variables: \npostPurchaseDto: {postPurchaseDto }')

		if isinstance (postPurchaseDto ,dict ):
			cpf =postPurchaseDto .get ('cpf')
			valor =postPurchaseDto .get ('valor',0 )
			is_delivery =postPurchaseDto .get ('is_delivery',False )
			is_from_client =postPurchaseDto .get ('isFromClient',False )
		else :
			cpf =getattr (postPurchaseDto ,'cpf',None )
			valor =getattr (postPurchaseDto ,'valor',0 )
			is_delivery =getattr (postPurchaseDto ,'is_delivery',False )
			is_from_client =getattr (postPurchaseDto ,'isFromClient',False )

		if not cpf or (isinstance (cpf ,str )and cpf .strip ()==""):
			cpf ="CPF NÃO INFORMADO"
			cliente ="CLIENTE NÃO INFORMADO"
			cliente_obj =None 
		else :

			cliente_obj =self .clienteRepository .get_cliente_by_cpf (cpf )

			if is_from_client and not cliente_obj :
				logger .info (f'Purchase originated from client and cliente not found for cpf {cpf }. Aborting create and returning info.')
				return {
				'created':False ,
				'cliente_exists':False ,
				'cpf':cpf ,
				'message':'Cliente não encontrado. Cadastre o cliente primeiro.'
				}
			cliente =cliente_obj .nome if cliente_obj else "CLIENTE NÃO ENCONTRADO"

		purchase_record =None 
		try :
			try :
				valor_float =float (valor )
			except Exception :
				valor_float =0.0 

			points_to_add =int (valor_float /15 )

			purchase_payload ={
			'cpf':cpf ,
			'cliente':cliente ,
			'valor':float (valor_float ),
			'is_delivery':bool (is_delivery ),
			'pontos_ganhos':points_to_add ,
			'data':datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")
			}

			if self .purchaseRepository and hasattr (self .purchaseRepository ,'create_purchase'):
				logger .info (f'Persisting purchase: {purchase_payload }')
				purchase_record =self .purchaseRepository .create_purchase (purchase_payload )

				created_flag =True 
			else :
				created_flag =False 
		except Exception as e :
			logger .error (f'Error persisting purchase: {e }')

		try :
			cliente =self .clienteRepository .get_cliente_by_cpf (cpf )
			if cliente :
				logger .info (f'Cliente found for cpf {cpf }: {cliente }')

				try :
					valor_float =float (valor )
				except Exception :
					valor_float =0.0 

				points_to_add =int (valor_float /15 )

				new_points =cliente .pontos +points_to_add 
				if new_points >10 :
					new_points =10 

				new_qtd_gasta =(cliente .qtd_gasta or 0 )+valor_float 

				updated_data ={
				'pontos':new_points ,
				'qtd_gasta':new_qtd_gasta ,
				'updated_at':datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")
				}

				logger .info (f'Updating cliente {cliente .id } with data: {updated_data }')
				updated =self .clienteRepository .update_cliente (cliente .id ,updated_data )

				return {
				'created':bool (purchase_record ),
				'purchase':purchase_record ,
				'cliente_updated':bool (updated ),
				'cliente_id':getattr (cliente ,'id',None ),
				'points_gained':points_to_add ,
				'new_points_total':new_points 
				}
			else :
				logger .info (f'No cliente found for cpf {cpf }. Purchase created (if repository supported), no cliente update.')
				return {
				'created':bool (purchase_record ),
				'purchase':purchase_record ,
				'cliente_updated':False ,
				'cliente_id':None ,
				'points_gained':points_to_add if 'points_to_add'in locals ()else 0 
				}
		except Exception as e :
			logger .error (f'Error while updating cliente for purchase: {e }')
			return {
			'purchase':purchase_record ,
			'cliente_updated':False ,
			'error':str (e )
			}

	def getAllPurchases (self ):
		logger .info ('In PurchaseService, method: getAllPurchases')
		try :
			if self .purchaseRepository and hasattr (self .purchaseRepository ,'get_all_purchases'):
				return self .purchaseRepository .get_all_purchases ()
			else :
				logger .warning ('No purchaseRepository or get_all_purchases not implemented. Returning empty list.')
				return []
		except Exception as e :
			logger .error (f'Error fetching purchases: {e }')
			return []

	def search_purchases (self ,query :str ):
		logger .info (f'In PurchaseService, method: search_purchases, variables: \n query: {query }')
		if not query :
			return self .getAllPurchases ()
		try :
			if self .purchaseRepository and hasattr (self .purchaseRepository ,'search_purchases'):
				return self .purchaseRepository .search_purchases (query )
			else :

				all_purchases =self .getAllPurchases ()
				q_lower =query .lower ()
				filtered =[p for p in all_purchases if (
				(p .get ('nome')and q_lower in str (p .get ('nome')).lower ())or 
				(p .get ('cpf')and q_lower in str (p .get ('cpf')).lower ())or 
				(p .get ('purchase_date')and q_lower in str (p .get ('purchase_date')).lower ())or 
				(p .get ('created_at')and q_lower in str (p .get ('created_at')).lower ())
				)]
				return filtered 
		except Exception as e :
			logger .error (f'Error searching purchases: {e }')
			return []

	def deletePurchaseById (self ,idPurchase :str ):
		logger .info (f'In PurchaseService, method: deletePurchaseById, variables: \nidPurchase: {idPurchase }')
		try :
			if self .purchaseRepository and hasattr (self .purchaseRepository ,'delete_purchase'):
				return self .purchaseRepository .delete_purchase (idPurchase )
			else :
				logger .warning ('No purchaseRepository or delete_purchase not implemented. Returning False.')
				return False 
		except Exception as e :
			logger .error (f'Error deleting purchase: {e }')
			return False 

