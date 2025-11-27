import logging 
from exceptions .ClienteNotFoundException import ClienteNotFoundException 
from models .Redeem import Redeem 
from datetime import datetime 
from dtos .RedeemDtos import CreateRedeemDto 
from typing import List 
from repositories .PrizeRepository import PrizeRepository 
from repositories .ClienteRepository import ClienteRepository 

logging .basicConfig (level =logging .INFO ,format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger =logging .getLogger (__name__ )

class RedeemService :
    def __init__ (self ,redeemRepository ,prizeRepository :PrizeRepository ,clienteRepository :ClienteRepository ):
        logger .info (f'Initiating RedeemService, variables: \nredeemRepository: {redeemRepository }')
        self .redeemRepository =redeemRepository 
        self .prizeRepository =prizeRepository 
        self .clienteRepository =clienteRepository 

    def createRedeem (self ,CreateRedeemDto ):
        logger .info (f'In RedeemService, method: createRedeem, variables: \nCreateRedeemDto: {CreateRedeemDto }')
        
        telefone = getattr(CreateRedeemDto, 'telefone', None)
        cliente = self .clienteRepository .get_cliente_by_phone (telefone )
        if not cliente :
            logger .error (f'Error finding cliente with phone {telefone }.')
            raise ClienteNotFoundException ()

        prizes =self .prizeRepository .get_all_prizes ()
        matching_prize =None 
        for prize in prizes :
            if prize .get ('pontos')==CreateRedeemDto .pontos :
                matching_prize =prize 
                break 

        if not matching_prize :
            logger .warning (f'No prize found for {CreateRedeemDto .pontos } points')
            return {
            'success':False ,
            'message':f'Nenhum prêmio encontrado para {CreateRedeemDto .pontos } pontos'
            }

        if cliente .pontos <CreateRedeemDto .pontos :
            logger .warning (f'Cliente {cliente .id } does not have enough points. Has: {cliente .pontos }, Needs: {CreateRedeemDto .pontos }')
            return {
            'success':False ,
            'message':f'Pontos insuficientes. Você tem {cliente .pontos } pontos e precisa de {CreateRedeemDto .pontos }'
            }

        redeemModel =Redeem (
        id =None ,
        cliente_id =cliente .id ,
        cliente_nome =cliente .nome ,
        cliente_telefone =cliente .telefone ,
        premio =matching_prize .get ('premio','Prêmio desconhecido'),
        pontos =CreateRedeemDto .pontos ,
        created_at =datetime .now ().strftime ("%Y-%m-%d %H:%M:%S"),
        updated_at =datetime .now ().strftime ("%Y-%m-%d %H:%M:%S"))

        response =self .redeemRepository .create_redeem (redeemModel )
        logger .info (f'Redeem created successfully. Response: {response }')

        updated_data ={
        'pontos':0 ,
        'updated_at':datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")
        }

        update_result =self .clienteRepository .update_cliente (cliente .id ,updated_data )

        if update_result :
            logger .info (f'Cliente {cliente .id } points reset to 0 after redeeming prize')
            return {
            'success':True ,
            'redeem':response ,
            'message':'Resgate realizado com sucesso'
            }
        else :
            logger .error (f'Failed to update cliente {cliente .id } points')
            return {
            'success':False ,
            'redeem':response ,
            'message':'Resgate registrado, mas erro ao atualizar pontos do cliente'
            }

    def getAllRedeems (self ):
        logger .info (f'In RedeemService, method: getAllRedeems')
        redeems =self .redeemRepository .get_all_redeems ()
        redeems_dto =[]
        for r in redeems :
            telefone = None
            cliente_nome = None
            try :
                cliente = self .clienteRepository .get_cliente_by_id (r .cliente_id )
                if cliente :
                    telefone = cliente .telefone
                    cliente_nome = cliente .nome
            except Exception :
                telefone = None
                cliente_nome = None

            redeems_dto .append ({
            "id":r .id ,
            "cliente_id":r .cliente_id ,
            "cliente_nome":cliente_nome ,
            "telefone":telefone ,
            "premio":r .premio ,
            "pontos":r .pontos ,
            "created_at":r .created_at 
            })

        return redeems_dto 

    def getRedeemsByCLienteId (self ,cliente_id :str )->List [dict ]:
        logger .info (f'In RedeemService, method: getRedeemsByCLienteId, variables: \ncliente_id: {cliente_id }')
        redeems =self .redeemRepository .get_redeems_by_cliente_id (cliente_id )
        # fetch cliente once to include telefone and nome
        telefone = None
        cliente_nome = None
        try :
            cliente = self .clienteRepository .get_cliente_by_id (cliente_id )
            if cliente :
                telefone = cliente .telefone
                cliente_nome = cliente .nome
        except Exception :
            telefone = None
            cliente_nome = None

        redeems_dto =[]
        for r in redeems :
            redeems_dto .append ({
            "id":r .id ,
            "cliente_id":r .cliente_id ,
            "cliente_nome":cliente_nome ,
            "telefone":telefone ,
            "premio":r .premio ,
            "pontos":r .pontos ,
            "created_at":r .created_at 
            })
        return redeems_dto 

    def updateRedeem (self ,idRedeem ,updateRedeemDto ):
            logger .info (f'In RedeemService, method: updateRedeem, variables: \nupdateRedeem: {updateRedeemDto }, idRedeem: {idRedeem }')

            redeem =self .redeemRepository .get_redeem_by_id (idRedeem )
            if not redeem :
                logger .error (f'Error finding the redeem with id {idRedeem }.')
                return None

            updatedData =updateRedeemDto .model_dump (exclude_none =True )

            updatedData ['updated_at']=datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")

            updatedRedeem =self .redeemRepository .update_redeem (idRedeem ,updatedData )

            logger .info (f'Redeem with id {idRedeem } updated successfully.')
            logger .info (f'\nUpdatedRedeem: {updatedRedeem }')
            return updatedRedeem 

    def deleteRedeemById (self ,idRedeem :str ):
        logger .info (f'In RedeemService, method: deleteRedeem, variables: \nidRedeem: {idRedeem }')
        redeem =self .redeemRepository .get_redeem_by_id (idRedeem )
        if not redeem :
            logger .error (f'Error finding redeem with ID {idRedeem } for deletion.')
            return False

        deletedRedeem =self .redeemRepository .delete_redeem (redeem .id )
        logger .info (f'Redeem with ID {idRedeem } deleted successfully.')
        return deletedRedeem 

    def search_redeems (self ,query :str )->List [dict ]:
        logger .info (f'In RedeemService, method: search_redeems, variables: \nquery: {query }')
        redeems =self .redeemRepository .search_redeems (query )
        redeems_dto =[]
        for r in redeems :
            telefone = None
            cliente_nome = None
            try :
                cliente = self .clienteRepository .get_cliente_by_id (r .cliente_id )
                if cliente :
                    telefone = cliente .telefone
                    cliente_nome = cliente .nome
            except Exception :
                telefone = None
                cliente_nome = None

            redeems_dto .append ({
            "id":r .id ,
            "cliente_id":r .cliente_id ,
            "cliente_nome":cliente_nome ,
            "telefone":telefone ,
            "premio":r .premio ,
            "pontos":r .pontos ,
            "created_at":r .created_at 
            })
        return redeems_dto 
