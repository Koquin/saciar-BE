from repositories.PurchaseRepository import PurchaseRepository
from services.PurchaseService import PurchaseService
from controllers.PurchaseController import PurchaseController
from fastapi import APIRouter, Query
db_name = "gerenciamento_clientes"
db_url = "mongodb://localhost:27017/"


purchaseRepository = PurchaseRepository(db_name, db_url)
purchaseService = PurchaseService(purchaseRepository)
purchaseController = PurchaseController(purchaseService)

router = APIRouter(prefix="/purchase", tags=["Purchases"])

@router.get("/", summary="Get all purchases", status_code=200)
def getAllPurchases():
    print("In PurchaseRouter, method: GetAllPurchases")
    response = purchaseController.getAllPurchases()
    return response


@router.post("/", summary="Create a new purchase", status_code=201)
def postPurchase(postPurchaseDto: dict):
    print(f'In PurchaseRouter, method: postPurchase, variables: \npostPurchaseDto: {postPurchaseDto}')
    response = purchaseController.postPurchase(postPurchaseDto)
    return response


@router.delete("/{idPurchase}", summary="Delete a purchase by ID", status_code=204)
def deletePurchase(idPurchase: str):
    print(f'In PurchaseRouter, method: deletePurchase, variables: \n idPurchase: {idPurchase}')
    response = purchaseController.deletePurchase(idPurchase)
    return response


@router.get("/search", summary="Search purchases", status_code=200)
def search_purchases(q: str = Query(None, description="Nome, CPF ou data para buscar")):
    print(f'In PurchaseRouter, method: search_purchases, variables: \nquery: {q}')
    return purchaseController.search_purchases(q)

