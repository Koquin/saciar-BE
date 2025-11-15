from typing import Union
from fastapi import FastAPI
from routers.AuthRouter import router as AuthRouter
from routers.ClienteRouter import router as ClienteRouter
from routers.PurchaseRouter import router as PurchaseRouter
from routers.PrizeRouter import router as PrizeRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title = "Gerenciamento de Clientes API", version = "1.0.0", description = "API para gerenciar clientes, incluindo autenticação e operações CRUD.")

# Para desenvolvimento em ambiente local, use as origens do seu app:
origins = [
    "http://localhost",  # Para testes locais no navegador
    "http://localhost:8000",
    "http://192.168.18.31:8000", # Seu IP de host (importante!)
    "http://10.0.2.2:8000",  # IP especial do emulador Android (AVD)
    # Adicione outras portas ou endereços IP, se necessário
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(AuthRouter)
app.include_router(ClienteRouter)
app.include_router(PurchaseRouter)
app.include_router(PrizeRouter)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Gerenciamento de Clientes API. Visit /docs for API documentation."}

