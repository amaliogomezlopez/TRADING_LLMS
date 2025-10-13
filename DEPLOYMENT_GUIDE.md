# 🚀 GUÍA DE DESPLIEGUE - Windows Server 24/7

## 📋 LISTA DE ARCHIVOS NECESARIOS

### **✅ Archivos ESENCIALES (obligatorios)**

```
TRADING_AI/
├── trading_bot.py              ← Bot original
├── model_comparison.py         ← Comparación de modelos
├── config.yml                  ← Configuración
├── .env                        ← API keys (CRÍTICO)
└── requirements.txt            ← Dependencias Python
```

### **📊 Archivos de ANÁLISIS (recomendados)**

```
├── analyze_models.py           ← Análisis de modelos
├── analyze_performance.py      ← Análisis de performance
├── analyze_by_period.py        ← Análisis por período
├── quick_compare.py            ← Comparación rápida
└── manage_logs.py              ← Gestión de logs
```

### **📚 Archivos de DOCUMENTACIÓN (opcionales)**

```
├── README.md
├── MODEL_COMPARISON_GUIDE.md
├── EXAMPLE_OUTPUT.md
├── CONFIG_GUIDE.md
└── MONITORING_GUIDE.md
```

### **🚫 Archivos que NO necesitas copiar**

```
.venv/                          ← Se crea en el servidor
__pycache__/                    ← Se genera automático
*.pyc                           ← Archivos compilados
.git/                           ← Opcional (si no usas git en servidor)
trading_log.csv                 ← Se generará nuevo
model_comparison.csv            ← Se generará nuevo
logs_backup/                    ← Se creará si es necesario
```

---

## 🔧 MÉTODO 1: TRANSFERENCIA MANUAL (RECOMENDADO)

### **Paso 1: Crear carpeta en el servidor**

En tu **Windows 10 server**, crea la carpeta:

```powershell
# Crear carpeta (ejemplo)
mkdir C:\TradingBot
cd C:\TradingBot
```

### **Paso 2: Copiar archivos esenciales**

**Opción A: USB/Red**
1. Copiar desde tu PC actual estos archivos:
   ```
   trading_bot.py
   model_comparison.py
   config.yml
   .env
   requirements.txt
   analyze_models.py
   analyze_performance.py
   quick_compare.py
   ```

2. Pegar en `C:\TradingBot\` del servidor

**Opción B: Compartir en red**
```powershell
# En tu PC actual, comparte la carpeta
# Luego en el servidor:
xcopy "\\TU_PC\TRADING_AI\*.py" "C:\TradingBot\" /Y
xcopy "\\TU_PC\TRADING_AI\*.yml" "C:\TradingBot\" /Y
xcopy "\\TU_PC\TRADING_AI\.env" "C:\TradingBot\" /Y
xcopy "\\TU_PC\TRADING_AI\requirements.txt" "C:\TradingBot\" /Y
```

### **Paso 3: Instalar Python en el servidor**

1. **Descargar Python 3.12.4** (o superior):
   - https://www.python.org/downloads/
   - ⚠️ **IMPORTANTE:** Durante instalación, marcar "Add Python to PATH"

2. **Verificar instalación:**
   ```powershell
   python --version
   # Debería mostrar: Python 3.12.4
   ```

### **Paso 4: Crear entorno virtual**

En el servidor:

```powershell
cd C:\TradingBot

# Crear entorno virtual
python -m venv .venv

# Activar entorno
.\.venv\Scripts\Activate.ps1
```

⚠️ **Si sale error de ejecución de scripts:**
```powershell
# Ejecutar como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Luego volver a intentar activar
.\.venv\Scripts\Activate.ps1
```

### **Paso 5: Instalar dependencias**

```powershell
# Con el entorno virtual activado
pip install -r requirements.txt

# O manualmente:
pip install python-binance groq python-dotenv pyyaml ta pandas numpy
```

### **Paso 6: Verificar API keys**

```powershell
# Ver contenido de .env (SIN mostrarlo en pantalla)
notepad .env
```

Debe contener:
```env
BINANCE_API_KEY=tu_api_key_aqui
BINANCE_API_SECRET=tu_secret_key_aqui
GROQ_API_KEY=tu_groq_key_aqui
```

### **Paso 7: Probar ejecución**

```powershell
# Prueba rápida (un ciclo)
python model_comparison.py
```

Si funciona correctamente, continúa al siguiente paso.

---

## 🔧 MÉTODO 2: CLONAR DESDE GITHUB (ALTERNATIVO)

### **Paso 1: Instalar Git en el servidor**

1. Descargar Git para Windows:
   - https://git-scm.com/download/win
   - Instalar con opciones por defecto

### **Paso 2: Clonar repositorio**

```powershell
cd C:\
git clone https://github.com/amaliogomezlopez/TRADING_LLMS.git TradingBot
cd TradingBot
```

### **Paso 3: Crear archivo .env**

⚠️ **CRÍTICO:** El `.env` NO está en GitHub (por seguridad)

```powershell
# Crear archivo .env
notepad .env
```

Pegar:
```env
BINANCE_API_KEY=tu_api_key_aqui
BINANCE_API_SECRET=tu_secret_key_aqui
GROQ_API_KEY=tu_groq_key_aqui
```

Guardar y cerrar.

### **Paso 4-7: Igual que Método 1**

Continuar desde "Crear entorno virtual" del Método 1.

---

## ⚙️ CONFIGURAR EJECUCIÓN 24/7

### **Opción A: Mantener terminal abierta (Simple)**

```powershell
# Activar entorno
.\.venv\Scripts\Activate.ps1

# Ejecutar bot
python model_comparison.py

# Minimizar ventana (NO cerrar)
```

**Ventajas:**
- ✅ Más simple
- ✅ Puedes ver output en tiempo real

**Desventajas:**
- ❌ Si cierras terminal, se detiene
- ❌ No se reinicia automáticamente

---

### **Opción B: Ejecutar como tarea programada (Recomendado)**

#### **1. Crear script de inicio**

Crear archivo `start_comparison.bat` en `C:\TradingBot\`:

```batch
@echo off
cd /d C:\TradingBot
call .venv\Scripts\activate.bat
python model_comparison.py
pause
```

#### **2. Configurar Tarea Programada**

1. Abrir **Programador de tareas** (Task Scheduler)
2. Crear tarea básica:
   - **Nombre:** Trading Bot Model Comparison
   - **Desencadenador:** Al iniciar el sistema
   - **Acción:** Iniciar un programa
   - **Programa:** `C:\TradingBot\start_comparison.bat`
   - **Iniciar en:** `C:\TradingBot`

3. Configuración avanzada:
   - ✅ Ejecutar aunque el usuario no haya iniciado sesión
   - ✅ Ejecutar con privilegios más altos
   - ✅ Configurar para: Windows 10
   - ✅ Si la tarea ya se está ejecutando: No iniciar nueva instancia

#### **3. Probar tarea**

- Clic derecho en la tarea → **Ejecutar**
- Verificar que `model_comparison.csv` se está generando

---

### **Opción C: Como servicio de Windows (Avanzado)**

Si quieres ejecutarlo como **servicio de Windows** (más robusto):

#### **1. Instalar NSSM (Non-Sucking Service Manager)**

```powershell
# Descargar NSSM desde: https://nssm.cc/download
# Extraer a C:\nssm\

# Ejecutar como Administrador
cd C:\nssm\win64

# Crear servicio
.\nssm.exe install TradingBotService "C:\TradingBot\.venv\Scripts\python.exe" "C:\TradingBot\model_comparison.py"
```

#### **2. Configurar servicio**

```powershell
# Directorio de trabajo
.\nssm.exe set TradingBotService AppDirectory "C:\TradingBot"

# Redirección de logs
.\nssm.exe set TradingBotService AppStdout "C:\TradingBot\service_output.log"
.\nssm.exe set TradingBotService AppStderr "C:\TradingBot\service_error.log"

# Reinicio automático
.\nssm.exe set TradingBotService AppExit Default Restart
```

#### **3. Iniciar servicio**

```powershell
# Iniciar
.\nssm.exe start TradingBotService

# Ver estado
.\nssm.exe status TradingBotService

# Detener (cuando necesites)
.\nssm.exe stop TradingBotService
```

---

## 📊 MONITOREO REMOTO

### **Opción 1: Escritorio Remoto**

```powershell
# Habilitar RDP en el servidor
# Panel de Control → Sistema → Configuración de Escritorio Remoto

# Conectar desde tu PC:
mstsc.exe
# IP del servidor: 192.168.X.X
```

### **Opción 2: Acceso por red compartida**

```powershell
# Compartir carpeta C:\TradingBot en red
# Acceder desde tu PC:
\\NOMBRE_SERVIDOR\TradingBot\model_comparison.csv
```

### **Opción 3: Copia automática de logs**

Crear tarea programada que copia logs cada hora:

**`sync_logs.bat`:**
```batch
@echo off
xcopy "C:\TradingBot\model_comparison.csv" "\\TU_PC\LogsBackup\" /Y
xcopy "C:\TradingBot\trading_log.csv" "\\TU_PC\LogsBackup\" /Y
```

---

## 🔍 VERIFICAR QUE TODO FUNCIONA

### **Checklist de verificación:**

```powershell
# 1. Python instalado
python --version

# 2. Entorno virtual activado
.\.venv\Scripts\Activate.ps1

# 3. Dependencias instaladas
pip list | Select-String "binance|groq|dotenv|yaml"

# 4. API keys configuradas
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('GROQ_API_KEY' if os.getenv('GROQ_API_KEY') else 'ERROR')"

# 5. Conexión a Binance
python -c "from binance.client import Client; import os; from dotenv import load_dotenv; load_dotenv(); client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'), testnet=True); print('OK' if client.get_account() else 'ERROR')"

# 6. Ejecución de bot
python model_comparison.py
# Esperar 2-3 minutos, luego Ctrl+C

# 7. Verificar archivo generado
dir model_comparison.csv
```

---

## 📁 ESTRUCTURA FINAL EN SERVIDOR

```
C:\TradingBot\
├── .venv\                      ← Entorno virtual (creado en servidor)
├── .env                        ← API keys (COPIAR desde PC)
├── config.yml                  ← Configuración (COPIAR)
├── requirements.txt            ← Dependencias (COPIAR)
├── model_comparison.py         ← Script principal (COPIAR)
├── trading_bot.py              ← Bot original (COPIAR)
├── analyze_models.py           ← Análisis (COPIAR)
├── analyze_performance.py      ← Análisis (COPIAR)
├── quick_compare.py            ← Comparación (COPIAR)
├── manage_logs.py              ← Gestión logs (COPIAR)
├── start_comparison.bat        ← Script inicio (CREAR en servidor)
├── model_comparison.csv        ← Se genera automáticamente
└── trading_log.csv             ← Se genera automáticamente
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### **Error: "python no se reconoce como comando"**
```powershell
# Agregar Python al PATH manualmente
setx PATH "%PATH%;C:\Users\TU_USUARIO\AppData\Local\Programs\Python\Python312"
```

### **Error: "No module named 'binance'"**
```powershell
# Verificar que el entorno virtual está activado
.\.venv\Scripts\Activate.ps1

# Reinstalar dependencias
pip install -r requirements.txt
```

### **Error: "cannot be loaded because running scripts is disabled"**
```powershell
# Ejecutar PowerShell como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Error: "BinanceAPIException: Invalid API-key"**
```powershell
# Verificar archivo .env
notepad .env

# Debe tener las 3 keys sin espacios ni comillas
```

### **El bot se detiene después de un tiempo**
```powershell
# Configurar para que el servidor no entre en suspensión
# Panel de Control → Opciones de energía → Nunca suspender
```

---

## 💾 BACKUP DE DATOS

### **Script automático de backup**

Crear `backup_logs.bat`:

```batch
@echo off
set timestamp=%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%
set timestamp=%timestamp: =0%

mkdir "C:\TradingBot\backups\%timestamp%"
xcopy "C:\TradingBot\*.csv" "C:\TradingBot\backups\%timestamp%\" /Y

echo Backup completado: %timestamp%
```

Ejecutar cada 24 horas con Tarea Programada.

---

## 🎯 RESUMEN RÁPIDO

### **Checklist de migración:**

- [ ] Copiar archivos esenciales (`.py`, `.yml`, `.env`, `requirements.txt`)
- [ ] Instalar Python 3.12+ en servidor
- [ ] Crear entorno virtual
- [ ] Instalar dependencias
- [ ] Verificar API keys en `.env`
- [ ] Probar ejecución manual
- [ ] Configurar inicio automático (Tarea Programada o Servicio)
- [ ] Configurar monitoreo remoto
- [ ] Configurar backup automático
- [ ] Verificar que no entre en suspensión

---

## 📞 COMANDOS ÚTILES

```powershell
# Ver proceso Python corriendo
Get-Process python

# Matar proceso si se cuelga
Stop-Process -Name python

# Ver logs en tiempo real (si usas servicio)
Get-Content C:\TradingBot\service_output.log -Wait

# Espacio en disco
Get-PSDrive C

# Tamaño de archivos CSV
(Get-Item C:\TradingBot\model_comparison.csv).Length / 1MB
```

---

🚀 **¡Con esta guía tu bot estará corriendo 24/7 en el servidor!**
