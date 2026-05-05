@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM QuizSnap - Script de inicio para Windows
REM ═══════════════════════════════════════════════════════════════════════════

echo.
echo ╔══════════════════════════════════════════════════════════════════════════╗
echo ║                    ⚡ QuizSnap - Iniciando...                            ║
echo ╚══════════════════════════════════════════════════════════════════════════╝
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] No se encontró el entorno virtual.
    echo.
    echo Por favor ejecuta primero:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Verificar si existe el archivo .env
if not exist ".env" (
    echo [ADVERTENCIA] No se encontró el archivo .env
    echo.
    echo Por favor configura tus API keys en el archivo .env
    echo.
    pause
)

REM Activar entorno virtual y ejecutar
call venv\Scripts\activate.bat
python quiz_solver.py

pause
