@echo off
echo ========================================
echo  INSTALACION DE DEPENDENCIAS
echo  Metodo alternativo sin compilacion
echo ========================================
echo.

REM Verificar que el entorno virtual esta activado
python -c "import sys; exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Entorno virtual no activado
    echo.
    echo Por favor ejecuta primero:
    echo   .\.venv\Scripts\Activate.ps1
    echo.
    pause
    exit /b 1
)

echo [1/3] Actualizando pip...
python -m pip install --upgrade pip

echo.
echo [2/3] Instalando dependencias sin compilacion...
echo.

REM Instalar dependencias una por una
echo - Instalando python-binance...
pip install python-binance

echo - Instalando groq...
pip install groq

echo - Instalando python-dotenv...
pip install python-dotenv

echo - Instalando pyyaml...
pip install pyyaml

echo - Instalando pandas (puede tardar)...
pip install pandas

echo - Instalando numpy...
pip install numpy

echo - Instalando ta (technical analysis)...
pip install ta

echo.
echo [3/3] Verificando instalacion...
echo.

python -c "import binance; import groq; import dotenv; import yaml; import pandas; import numpy; import ta; print('✓ Todas las dependencias instaladas correctamente')" 2>nul
if errorlevel 1 (
    echo ERROR: Algunas dependencias fallaron
    echo.
    echo Ejecuta manualmente:
    echo   pip list
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  INSTALACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Puedes ejecutar el bot con:
echo   python model_comparison.py
echo   python trading_bot.py
echo.
pause
