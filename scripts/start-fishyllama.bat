@echo off
setlocal
cd /d "%~dp0.."
if not exist .venv python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m uvicorn backend.web:app --host 0.0.0.0 --port %FISHYLLAMA_PORT%
if errorlevel 1 python -m uvicorn backend.web:app --host 0.0.0.0 --port 8000
