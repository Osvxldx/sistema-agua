@echo off
title Sistema de Agua Potable

REM Verificar si Python está disponible
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python no encontrado
    echo.
    echo Por favor ejecute install.bat primero
    echo o instale Python desde python.org
    echo.
    pause
    exit /b 1
)

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Ejecutar el sistema
echo Iniciando Sistema de Agua Potable...
python main.py

REM Si hay error, mostrar mensaje
if %ERRORLEVEL% neq 0 (
    echo.
    echo Error al ejecutar el sistema
    echo Verifique la documentación o contacte soporte
    echo.
    pause
)