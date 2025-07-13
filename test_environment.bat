@echo off
echo Starting Python environment test...

python --version
echo.

echo Testing imports...
python -c "import fastapi; print('FastAPI OK')"
python -c "import uvicorn; print('Uvicorn OK')"
python -c "from app.config import SECRET_KEY; print('Config OK')"
python -c "from app.utils import load_movies; print('Utils OK')"

echo.
echo Starting minimal server...
python minimal_server_test.py

pause
