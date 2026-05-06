@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM QuizSnap - Script para detener la aplicación
REM ═══════════════════════════════════════════════════════════════════════════

echo.
echo ╔══════════════════════════════════════════════════════════════════════════╗
echo ║                    ⚡ QuizSnap - Deteniendo...                           ║
echo ╚══════════════════════════════════════════════════════════════════════════╝
echo.

REM Buscar y terminar el proceso pythonw.exe que ejecuta quiz_solver.py
tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I /N "pythonw.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [INFO] Deteniendo QuizSnap...
    taskkill /F /IM pythonw.exe >NUL 2>&1
    echo [OK] QuizSnap detenido correctamente.
) else (
    echo [INFO] QuizSnap no está en ejecución.
)

echo.
timeout /t 2 >nul
exit
