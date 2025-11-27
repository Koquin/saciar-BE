from fastapi import APIRouter 
from controllers .RedeemController import RedeemController 
from repositories .RedeemRepository import RedeemRepository 
from repositories .PrizeRepository import PrizeRepository 
from repositories .ClienteRepository import ClienteRepository 
from services .RedeemService import RedeemService 
from dtos .RedeemDtos import CreateRedeemDto ,UpdateRedeemDto 
from typing import List 
from fastapi import Query 

db_name ="gerenciamento_clientes"
db_url ="mongodb://localhost:27017/"

redeemRepository =RedeemRepository (db_name ,db_url )
prizeRepository =PrizeRepository (db_name ,db_url )
clienteRepository =ClienteRepository (db_name ,db_url )
redeemService =RedeemService (redeemRepository ,prizeRepository ,clienteRepository )
redeemController =RedeemController (redeemService )

router =APIRouter (prefix ="/redeems",tags =["Redeems"])

@router .post ("/",summary ="Create a new redeem",status_code =201 )
def postRedeem (CreateRedeemDto :CreateRedeemDto ):
    print (f'In RedeemRouter, method: postRedeem, variables: \nCreateRedeemDto: {CreateRedeemDto }')
    response =redeemController .postRedeem (CreateRedeemDto )
    print("Response: ", response)
    return response 

@router .get ("/",summary ="Get all redeems",status_code =200 )
def getAllRedeems ():
    print (f'In RedeemRouter, method: getAllRedeems')
    response =redeemController .getAllRedeems ()
    print("Response: ", response)
    return response 

@router .get ("/cliente/{cliente_id}",summary ="Get redeems by cliente ID",status_code =200 )
def getRedeemsByClienteId (cliente_id :str ):
    print (f'In RedeemRouter, method: getRedeemsByClienteId, variables: \ncliente_id: {cliente_id }')
    response =redeemController .getRedeemsByClienteId (cliente_id )
    return response 

@router .put ("/{idRedeem}",summary ="Update a redeem by ID",status_code =200 )
def updateRedeem (idRedeem ,atualizarRedeemDto :UpdateRedeemDto ):
    print (f'In RedeemRouter, method: updateRedeem, variables: \nidRedeem: {idRedeem }, atualizarRedeemDto: {atualizarRedeemDto }')
    response =redeemController .updateRedeem (idRedeem ,atualizarRedeemDto )
    return response 

@router .delete ("/{idRedeem}",summary ="Delete a redeem by ID",status_code =204 )
def deleteRedeem (idRedeem ):
    print (f'In RedeemRouter, method: deleteRedeem, variables: \n idRedeem: {idRedeem }')
    response =redeemController .deleteRedeem (idRedeem )
    return response 

@router .get ("/search",response_model =List [dict ],summary ="Search redeems")
def search_redeems (q :str =Query (None ,description ="Prêmio ou cliente_id para buscar")):
    print (f'In RedeemRouter, method: search_redeems, variables: \nquery: {q }')
    response = redeemController .search_redeems (q )
    print("Response: ", response)
    return response
