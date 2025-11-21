from fastapi import APIRouter 
from typing import List 
from repositories .PrizeRepository import PrizeRepository 
from services .PrizeService import PrizeService 
from controllers .PrizeController import PrizeController 
from dtos .ClienteDtos import UsePointsDto 
db_name ="gerenciamento_clientes"
db_url ="mongodb://localhost:27017/"

prizeRepository =PrizeRepository (db_name ,db_url )
prizeService =PrizeService (prizeRepository )
prizeController =PrizeController (prizeService )

router =APIRouter (prefix ="/prizes",tags =["Prizes"])

@router .get ("/",summary ="Get all prizes",status_code =200 )
def getAllPrizes ():
	print ("In PrizeRouter, method: getAllPrizes")
	response = prizeController.get_all_prizes ()
	return response 


@router .put ("/",summary ="Update the full list of prizes",status_code =200 )
def putPrizes (prizes :List [dict ]):
	print (f'In PrizeRouter, method: putPrizes, variables: \nprizes: {prizes }')
	success =prizeController.update_prizes (prizes )
	return {"success":bool (success )}


@router .post ("/usepoints",summary ="Use points to redeem a prize",status_code =200 )
def usePoints (usePointsDto :UsePointsDto ):
	print (f'In PrizeRouter, method: usePoints, variables: \nusePointsDto: {usePointsDto }')
	response =prizeController.use_points (usePointsDto .cliente_id ,usePointsDto .points )
	return response 

