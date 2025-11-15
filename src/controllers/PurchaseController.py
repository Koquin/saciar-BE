from dtos.purchaseDtos import postPurchaseDto
from fastapi.responses import JSONResponse

class PurchaseController:
	def __init__(self, purchaseService):
		print(f'Initiating PurchaseController, variables: \npurchaseService: {purchaseService}')
		self.purchaseService = purchaseService

	def postPurchase(self, postPurchaseDto: dict):
		print(f'In PurchaseController, method: postPurchase, variables: \npostPurchaseDto: {postPurchaseDto}')
		response = self.purchaseService.createPurchase(postPurchaseDto)
		# If service indicates it actually created the purchase, return 201 Created
		if isinstance(response, dict) and response.get('created'):
			return JSONResponse(response, status_code=201)
		# otherwise return 200 so frontend can react (e.g. prompt to register cliente)
		return JSONResponse(response, status_code=200)

	def getAllPurchases(self):
		print(f'In PurchaseController, method: getAllPurchases')
		response = self.purchaseService.getAllPurchases()
		return response

	def search_purchases(self, query: str):
		print(f'In PurchaseController, method: search_purchases, variables: \n query: {query}')
		return self.purchaseService.search_purchases(query)

	def deletePurchase(self, idPurchase: str):
		print(f'In PurchaseController, method: deletePurchase, variables: \n idPurchase: {idPurchase}')
		response = self.purchaseService.deletePurchaseById(idPurchase)
		return response

