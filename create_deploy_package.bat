@echo off
echo ========================================
echo  PREPARANDO PAQUETE DE DESPLIEGUE
echo ========================================
echo.

REM Crear carpeta de despliegue
if exist deploy_package rmdir /s /q deploy_package
mkdir deploy_package

echo [1/4] Copiando scripts Python...
copy trading_bot.py deploy_package\ >nul 2>&1
copy model_comparison.py deploy_package\ >nul 2>&1
copy analyze_models.py deploy_package\ >nul 2>&1
copy analyze_performance.py deploy_package\ >nul 2>&1
copy analyze_by_period.py deploy_package\ >nul 2>&1
copy quick_compare.py deploy_package\ >nul 2>&1
copy manage_logs.py deploy_package\ >nul 2>&1

echo [2/4] Copiando archivos de configuracion...
copy config.yml deploy_package\ >nul 2>&1
copy .env deploy_package\ >nul 2>&1
copy requirements.txt deploy_package\ >nul 2>&1

echo [3/4] Copiando documentacion...
copy README.md deploy_package\ >nul 2>&1
copy MODEL_COMPARISON_GUIDE.md deploy_package\ >nul 2>&1
copy DEPLOYMENT_GUIDE.md deploy_package\ >nul 2>&1
copy FILES_TO_DEPLOY.md deploy_package\ >nul 2>&1

echo [4/4] Creando script de inicio para servidor...

REM Crear start_comparison.bat en deploy_package
echo @echo off > deploy_package\start_comparison.bat
echo cd /d %%~dp0 >> deploy_package\start_comparison.bat
echo call .venv\Scripts\activate.bat >> deploy_package\start_comparison.bat
echo python model_comparison.py >> deploy_package\start_comparison.bat
echo pause >> deploy_package\start_comparison.bat

REM Crear start_trading_bot.bat en deploy_package
echo @echo off > deploy_package\start_trading_bot.bat
echo cd /d %%~dp0 >> deploy_package\start_trading_bot.bat
echo call .venv\Scripts\activate.bat >> deploy_package\start_trading_bot.bat
echo python trading_bot.py >> deploy_package\start_trading_bot.bat
echo pause >> deploy_package\start_trading_bot.bat

REM Crear README para el servidor
echo # INSTRUCCIONES DE INSTALACION > deploy_package\INSTALL.txt
echo. >> deploy_package\INSTALL.txt
echo 1. Instalar Python 3.12+ desde https://www.python.org/downloads/ >> deploy_package\INSTALL.txt
echo    IMPORTANTE: Marcar "Add Python to PATH" durante instalacion >> deploy_package\INSTALL.txt
echo. >> deploy_package\INSTALL.txt
echo 2. Abrir PowerShell como Administrador en esta carpeta >> deploy_package\INSTALL.txt
echo. >> deploy_package\INSTALL.txt
echo 3. Ejecutar: >> deploy_package\INSTALL.txt
echo    python -m venv .venv >> deploy_package\INSTALL.txt
echo    .\.venv\Scripts\Activate.ps1 >> deploy_package\INSTALL.txt
echo    pip install -r requirements.txt >> deploy_package\INSTALL.txt
echo. >> deploy_package\INSTALL.txt
echo 4. Verificar archivo .env con tus API keys >> deploy_package\INSTALL.txt
echo. >> deploy_package\INSTALL.txt
echo 5. Ejecutar bot: >> deploy_package\INSTALL.txt
echo    - Comparacion de modelos: start_comparison.bat >> deploy_package\INSTALL.txt
echo    - Bot original: start_trading_bot.bat >> deploy_package\INSTALL.txt
echo. >> deploy_package\INSTALL.txt
echo Ver DEPLOYMENT_GUIDE.md para configuracion 24/7 >> deploy_package\INSTALL.txt

echo.
echo ========================================
echo  PAQUETE CREADO EXITOSAMENTE
echo ========================================
echo.
echo Carpeta: deploy_package\
echo.
echo Contenido:
dir /b deploy_package
echo.
echo SIGUIENTE PASO:
echo.
echo 1. Copiar carpeta "deploy_package" a USB o red
echo 2. En el servidor, renombrar a "TradingBot"
echo 3. Seguir instrucciones en INSTALL.txt
echo.
echo ========================================
pause
