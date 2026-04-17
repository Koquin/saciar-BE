import logging
from datetime import datetime
from typing import Optional

from ..repositories.ClienteRepository import ClienteRepository 

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
			telefone =postPurchaseDto .get ('telefone')
			valor =postPurchaseDto .get ('valor',0 )
			is_delivery =postPurchaseDto .get ('is_delivery',False )
			is_from_client =postPurchaseDto .get ('isFromClient',False )
		else :
			telefone =getattr (postPurchaseDto ,'telefone',None )
			valor =getattr (postPurchaseDto ,'valor',0 )
			is_delivery =getattr (postPurchaseDto ,'is_delivery',False )
			is_from_client =getattr (postPurchaseDto ,'isFromClient',False )

		if not telefone or (isinstance (telefone ,str )and telefone .strip ()==""):
			telefone ="TELEFONE NÃO INFORMADO"
			cliente ="CLIENTE NÃO INFORMADO"
			cliente_obj =None 
		else :

			cliente_obj =self .clienteRepository .get_cliente_by_phone (telefone )

			if is_from_client and not cliente_obj :
				logger .info (f'Purchase originated from client and cliente not found for phone {telefone }. Aborting create and returning info.')
				return {
				'created':False ,
				'cliente_exists':False ,
				'telefone':telefone ,
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
			'telefone':telefone ,
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
			cliente =self .clienteRepository .get_cliente_by_phone (telefone )
			if cliente :
				logger .info (f'Cliente found for phone {telefone }: {cliente }')

				try :
					valor_float =float (valor )
				except Exception :
					valor_float =0.0 

				# Add existing troco to purchase value
				troco_atual = getattr(cliente, 'troco', 0.0) or 0.0
				valor_total_com_troco = valor_float + troco_atual

				# Calculate points from total (including troco)
				points_to_add = int(valor_total_com_troco / 15)
				# Calculate remaining troco (modulo operation)
				novo_troco = valor_total_com_troco % 15

				logger .info (f'Purchase calculation: valor={valor_float}, troco_atual={troco_atual}, valor_total={valor_total_com_troco}, points={points_to_add}, novo_troco={novo_troco}')

				new_points = cliente .pontos + points_to_add 
				if new_points > 10 :
					new_points = 10 

				new_qtd_gasta = (cliente .qtd_gasta or 0 ) + valor_float 

				updated_data = {
				'pontos': new_points ,
				'qtd_gasta': new_qtd_gasta ,
				'troco': novo_troco ,
				'updated_at': datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")
				}

				logger .info (f'Updating cliente {cliente .id } with data: {updated_data }')
				updated = self .clienteRepository .update_cliente (cliente .id , updated_data )

				return {
				'created': bool (purchase_record ),
				'purchase': purchase_record ,
				'cliente_updated': bool (updated ),
				'cliente_id': getattr (cliente , 'id', None ),
				'points_gained': points_to_add ,
				'new_points_total': new_points ,
				'new_troco': novo_troco
				}
			else :
				logger .info (f'No cliente found for phone {telefone }. Purchase created (if repository supported), no cliente update.')
				return {
				'created': bool (purchase_record ),
				'purchase': purchase_record ,
				'cliente_updated': False ,
				'cliente_id': None ,
				'points_gained': points_to_add if 'points_to_add' in locals () else 0 
				}
		except Exception as e :
			logger .error (f'Error while updating cliente for purchase: {e }')
			return {
			'purchase': purchase_record ,
			'cliente_updated': False ,
			'error': str (e )
			}

	def getAllPurchases (self ):
		logger .info ('In PurchaseService, method: getAllPurchases')
		try :
			if self .purchaseRepository and hasattr (self .purchaseRepository ,'get_all_purchases'):
				result = self .purchaseRepository .get_all_purchases ()
				logger .info (f'PurchaseService returning {len (result )} purchases')
				return result
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
				(p .get ('telefone')and q_lower in str (p .get ('telefone')).lower ())or 
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

