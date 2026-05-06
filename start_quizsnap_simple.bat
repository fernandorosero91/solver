@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM QuizSnap - Inicio simple (minimizado)
REM ═══════════════════════════════════════════════════════════════════════════

REM Ejecutar minimizado
start /MIN "" cmd /c "cd /d "%~dp0" && venv\Scripts\python.exe quiz_solver.py"

echo QuizSnap iniciado (ventana minimizada)
timeout /t 2 >nul
exit
