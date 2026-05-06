@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM QuizSnap - Script de inicio con ventana visible (para debugging)
REM ═══════════════════════════════════════════════════════════════════════════

echo.
echo ╔══════════════════════════════════════════════════════════════════════════╗
echo ║                    ⚡ QuizSnap - Modo Debug                              ║
echo ╚══════════════════════════════════════════════════════════════════════════╝
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\python.exe" (
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
    echo Por favor configura tus API keys en el archivo .env
    echo.
    pause
)

echo [INFO] Iniciando QuizSnap en modo debug...
echo [INFO] La ventana permanecerá abierta para ver logs
echo [INFO] Presiona Ctrl+Shift+X para salir
echo.

REM Ejecutar con ventana visible
venv\Scripts\python.exe quiz_solver.py

echo.
echo [INFO] QuizSnap cerrado.
pause
