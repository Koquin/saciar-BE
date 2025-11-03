from fastapi import APIRouter
from controllers.AuthController import AuthController
from repositories.AuthRepository import AuthRepository
from services.AuthService import AuthService
from dtos import authDtos
db_name = "gerenciamento_clientes"
db_url = "mongodb://localhost:27017/"

authRepository = AuthRepository(db_name, db_url)
authService = AuthService(authRepository)
authController = AuthController(authService)

router = APIRouter(prefix="/auth", tags=["Authentication"])
    
@router.post("/login", summary="Authenticate user", status_code=200)
def login(authDto: authDtos.authDto):
    print(f'In AuthRouter, method: login, variables: \nauthDto: {authDto}')
    try:
        response =  authController.login(authDto)
        return response
    except Exception as e:
        raise e

