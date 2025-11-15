import logging 
from typing import Optional 
from repositories .PrizeRepository import PrizeRepository 
from repositories .ClienteRepository import ClienteRepository 
from exceptions .ClienteNotFoundException import ClienteNotFoundException 

logging .basicConfig (level =logging .INFO ,format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger =logging .getLogger (__name__ )


class PrizeService :
    def __init__ (self ,prizeRepository :PrizeRepository ,db_name :str ="gerenciamento_clientes",db_url :str ="mongodb://localhost:27017/"):
        logger .info (f'Initiating PrizeService, variables: \nprizeRepository: {prizeRepository }')
        self .prizeRepository =prizeRepository 
        self .clienteRepository =ClienteRepository (db_name ,db_url )

    def get_all_prizes (self ):
        logger .info ('In PrizeService, method: get_all_prizes')
        try :
            if self .prizeRepository and hasattr (self .prizeRepository ,'get_all_prizes'):
                return self .prizeRepository .get_all_prizes ()
            return []
        except Exception as e :
            logger .error (f'Error getting prizes: {e }')
            return []

    def update_prizes (self ,prizes_list :list )->bool :
        logger .info (f'In PrizeService, method: update_prizes, variables: \nprizes_list: {prizes_list }')
        try :
            if self .prizeRepository and hasattr (self .prizeRepository ,'update_prizes'):
                return self .prizeRepository .update_prizes (prizes_list )
            return False 
        except Exception as e :
            logger .error (f'Error updating prizes: {e }')
            return False 

    def use_points (self ,cliente_id :str ,points :int ):
        logger .info (f'In PrizeService, method: use_points, variables: \ncliente_id: {cliente_id }, points: {points }')
        try :

            prizes =self .get_all_prizes ()
            logger .info (f'Retrieved prizes: {prizes }')


            matching_prize =None 
            for prize in prizes :
                if prize .get ('pontos')==points :
                    matching_prize =prize 
                    break 

            if not matching_prize :
                logger .warning (f'No prize found for {points } points')
                return {
                'success':False ,
                'message':f'Nenhum prêmio encontrado para {points } pontos'
                }


            cliente =self .clienteRepository .get_cliente_by_id (cliente_id )
            if not cliente :
                logger .error (f'Cliente not found with ID: {cliente_id }')
                raise ClienteNotFoundException ()


            if cliente .pontos <points :
                logger .warning (f'Cliente {cliente_id } does not have enough points. Has: {cliente .pontos }, Needs: {points }')
                return {
                'success':False ,
                'message':f'Pontos insuficientes. Você tem {cliente .pontos } pontos e precisa de {points }'
                }


            updated_data ={
            'pontos':0 ,
            'updated_at':__import__ ('datetime').datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")
            }

            update_result =self .clienteRepository .update_cliente (cliente .id ,updated_data )

            if update_result :
                logger .info (f'Cliente {cliente_id } points reset to 0 after redeeming prize')
                return {
                'success':True ,
                'pontos':points ,
                'premio':matching_prize .get ('premio','Prêmio desconhecido')
                }
            else :
                logger .error (f'Failed to update cliente {cliente_id } points')
                return {
                'success':False ,
                'message':'Erro ao atualizar pontos do cliente'
                }

        except ClienteNotFoundException :
            logger .error (f'Cliente not found with ID: {cliente_id }')
            return {
            'success':False ,
            'message':f'Cliente com ID {cliente_id } não encontrado'
            }
        except Exception as e :
            logger .error (f'Error using points: {e }')
            return {
            'success':False ,
            'message':f'Erro ao processar pontos: {str (e )}'
            }
