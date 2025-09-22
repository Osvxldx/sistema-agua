@echo off
echo ========================================
echo    INSTALADOR DEL SISTEMA DE AGUA POTABLE
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python no está instalado en este sistema.
    echo.
    echo Por favor:
    echo 1. Descargue Python desde https://python.org
    echo 2. Instálelo marcando "Add Python to PATH"
    echo 3. Ejecute este instalador nuevamente
    echo.
    pause
    exit /b 1
)

echo ✓ Python detectado correctamente
echo.

REM Verificar si pip está disponible
pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: pip no está disponible.
    echo Reinstale Python con la opción "Add Python to PATH"
    pause
    exit /b 1
)

echo ✓ pip detectado correctamente
echo.

echo Instalando dependencias...
echo.

REM Instalar dependencias
pip install reportlab Pillow python-dateutil

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: No se pudieron instalar todas las dependencias.
    echo Verifique su conexión a internet e intente nuevamente.
    pause
    exit /b 1
)

echo.
echo ✓ Dependencias instaladas correctamente
echo.

REM Crear carpetas necesarias
if not exist "recibos" mkdir recibos
echo ✓ Carpetas creadas

echo.
echo ========================================
echo    INSTALACIÓN COMPLETADA
echo ========================================
echo.
echo El sistema está listo para usar.
echo.
echo Para iniciar el sistema:
echo   - Ejecute: python main.py
echo   - O haga doble clic en main.py
echo.
echo PIN por defecto: 1234
echo.
echo ¡IMPORTANTE!
echo - Cambie el PIN desde Configuración
echo - Cree respaldos regulares
echo - Lea el archivo README.md
echo.
pause