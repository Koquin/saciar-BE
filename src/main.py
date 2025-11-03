from typing import Union
from fastapi import FastAPI
from routers.AuthRouter import router as AuthRouter
from routers.ClienteRouter import router as ClienteRouter
app = FastAPI(title = "Gerenciamento de Clientes API", version = "1.0.0", description = "API para gerenciar clientes, incluindo autenticação e operações CRUD.")

app.include_router(AuthRouter)
app.include_router(ClienteRouter)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Gerenciamento de Clientes API. Visit /docs for API documentation."}

