from dtos .RedeemDtos import CreateRedeemDto 
from typing import List 

class RedeemController :
    def __init__ (self ,redeemService ):
        print (f'Initiating RedeemController, variables: \nredeemService: {redeemService }')
        self .redeemService =redeemService 

    def postRedeem (self ,CreateRedeemDto ):
        print (f'In RedeemController, method: postRedeem, variables: \nCreateRedeemDto: {CreateRedeemDto }')
        response =self .redeemService .createRedeem (CreateRedeemDto )
        return response 

    def getAllRedeems (self ):
        print (f'In RedeemController, method: getAllRedeems')
        response =self .redeemService .getAllRedeems ()
        return response 

    def getRedeemsByClienteId (self ,cliente_id :str )->List [dict ]:
        print (f'In RedeemController, method: getRedeemsByClienteId, variables: \ncliente_id: {cliente_id }')
        response =self .redeemService .getRedeemsByCLienteId (cliente_id )
        return response 

    def updateRedeem (self ,idRedeem ,atualizarRedeemDto ):
        print (f'In RedeemController, method: updateRedeem, variables: \nidRedeem: {idRedeem }, atualizarRedeemDto: {atualizarRedeemDto }')
        return self .redeemService .updateRedeem (idRedeem ,atualizarRedeemDto )

    def deleteRedeem (self ,idRedeem :str ):
        print (f'In RedeemController, method: deleteRedeem, variables: \n idRedeem: {idRedeem }')
        response =self .redeemService .deleteRedeemById (idRedeem )
        return response 

    def search_redeems (self ,query :str )->List [dict ]:
        if not query :
            return self .getAllRedeems ()
        return self .redeemService .search_redeems (query )
