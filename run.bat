@echo off

REM Ativa o ambiente virtual
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo Erro ao ativar o ambiente virtual.
    exit /b 1
)

echo Installing dependencies...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo Erro ao instalar as dependencias.
    exit /b 1
)

echo.
echo Starting API server...
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
