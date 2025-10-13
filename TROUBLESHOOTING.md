# 🔧 SOLUCIÓN DE PROBLEMAS - Instalación en Windows

## ❌ Error: "Unknown compiler(s)" o "Could not find vswhere.exe"

### **Problema:**
Pandas/Numpy intentan compilarse desde el código fuente y faltan herramientas de C++.

### **Solución 1: Usar versiones pre-compiladas (RECOMENDADO)**

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Actualizar pip
python -m pip install --upgrade pip

# Instalar sin versiones específicas
pip install python-binance groq python-dotenv pyyaml pandas numpy ta
```

**O usar el script automático:**
```powershell
.\install_dependencies.bat
```

---

### **Solución 2: Usar requirements simplificado**

```powershell
pip install -r requirements_simple.txt
```

---

### **Solución 3: Instalar Microsoft Visual C++ (si necesitas versiones específicas)**

1. **Descargar Visual Studio Build Tools:**
   - https://visualstudio.microsoft.com/downloads/
   - Buscar "Build Tools for Visual Studio 2022"

2. **Durante instalación, seleccionar:**
   - ✅ Desktop development with C++
   - ✅ MSVC v143 - VS 2022 C++ x64/x86 build tools
   - ✅ Windows 10 SDK

3. **Reiniciar terminal y ejecutar:**
   ```powershell
   pip install -r requirements.txt
   ```

---

## ❌ Error: "pip no se reconoce como comando"

### **Solución:**

```powershell
# Verificar que Python está en PATH
python --version

# Usar python -m pip en lugar de pip
python -m pip install -r requirements.txt
```

---

## ❌ Error: "running scripts is disabled on this system"

### **Problema:**
PowerShell no permite ejecutar scripts.

### **Solución:**

```powershell
# Ejecutar PowerShell como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Intentar de nuevo
.\.venv\Scripts\Activate.ps1
```

---

## ❌ Error: "ModuleNotFoundError: No module named 'binance'"

### **Problema:**
Entorno virtual no activado o dependencias no instaladas.

### **Solución:**

```powershell
# 1. Verificar que estás en el entorno virtual
# Debería aparecer (.venv) al inicio de la línea

# 2. Activar si no está activo
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install python-binance groq python-dotenv pyyaml pandas numpy ta
```

---

## ❌ Error: "AttributeError: module 'numpy' has no attribute 'X'"

### **Problema:**
Versión de numpy incompatible con pandas.

### **Solución:**

```powershell
# Desinstalar versiones antiguas
pip uninstall numpy pandas -y

# Instalar versiones compatibles
pip install numpy pandas
```

---

## ❌ Error: "BinanceAPIException: Invalid API-key"

### **Problema:**
API keys incorrectas o archivo .env mal configurado.

### **Solución:**

```powershell
# 1. Verificar archivo .env
notepad .env

# Debe tener este formato (sin espacios ni comillas):
BINANCE_API_KEY=tu_clave_aqui
BINANCE_API_SECRET=tu_secreto_aqui
GROQ_API_KEY=tu_groq_key_aqui

# 2. Verificar que está en la carpeta correcta
dir .env

# 3. Probar carga de variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', os.getenv('BINANCE_API_KEY')[:10] + '...')"
```

---

## ❌ Error al ejecutar: "FileNotFoundError: [Errno 2] No such file or directory: 'config.yml'"

### **Problema:**
Archivo config.yml no existe o estás en la carpeta incorrecta.

### **Solución:**

```powershell
# 1. Verificar que config.yml existe
dir config.yml

# 2. Si no existe, crearlo desde config.example.yml
copy config.example.yml config.yml

# 3. O descargar desde GitHub
# https://github.com/amaliogomezlopez/TRADING_LLMS/blob/main/config.yml
```

---

## ⚠️ Python 3.13+ instalado

### **Problema:**
Algunas librerías aún no tienen wheels para Python 3.13.

### **Solución:**

Desinstalar Python 3.13 e instalar **Python 3.12.4**:
- https://www.python.org/downloads/release/python-3124/
- Durante instalación: ✅ Add Python to PATH

---

## 🔧 COMANDOS DE DIAGNÓSTICO

### **Verificar versiones:**
```powershell
python --version
pip --version
```

### **Ver dependencias instaladas:**
```powershell
pip list
```

### **Ver ubicación de Python:**
```powershell
python -c "import sys; print(sys.executable)"
```

### **Verificar entorno virtual activo:**
```powershell
python -c "import sys; print('Virtual Env' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 'System Python')"
```

### **Probar importaciones:**
```powershell
python -c "import binance, groq, dotenv, yaml, pandas, numpy, ta; print('✓ All OK')"
```

---

## 📋 INSTALACIÓN LIMPIA (desde cero)

Si nada funciona, empezar de cero:

```powershell
# 1. Eliminar entorno virtual antiguo
Remove-Item -Recurse -Force .venv

# 2. Crear nuevo entorno virtual
python -m venv .venv

# 3. Activar
.\.venv\Scripts\Activate.ps1

# 4. Actualizar pip
python -m pip install --upgrade pip

# 5. Instalar dependencias sin versiones fijas
pip install python-binance groq python-dotenv pyyaml pandas numpy ta

# 6. Verificar
pip list
```

---

## 🆘 SOLUCIÓN RÁPIDA (método alternativo)

Si sigues teniendo problemas, usa **Anaconda/Miniconda** en lugar de venv:

### **1. Descargar Miniconda:**
- https://docs.conda.io/en/latest/miniconda.html

### **2. Crear entorno con conda:**
```powershell
conda create -n trading_bot python=3.12
conda activate trading_bot
```

### **3. Instalar dependencias:**
```powershell
conda install pandas numpy
pip install python-binance groq python-dotenv pyyaml ta
```

### **4. Ejecutar bot:**
```powershell
python model_comparison.py
```

---

## 📞 INFORMACIÓN DEL SISTEMA

Para reportar un problema, ejecuta:

```powershell
echo "=== SYSTEM INFO ===" > system_info.txt
echo Python Version: >> system_info.txt
python --version >> system_info.txt
echo. >> system_info.txt
echo Pip Version: >> system_info.txt
pip --version >> system_info.txt
echo. >> system_info.txt
echo Installed Packages: >> system_info.txt
pip list >> system_info.txt
echo. >> system_info.txt
echo OS Info: >> system_info.txt
systeminfo | findstr /C:"OS" >> system_info.txt

notepad system_info.txt
```

---

🚀 **Con estas soluciones deberías poder instalar todo sin problemas!**
