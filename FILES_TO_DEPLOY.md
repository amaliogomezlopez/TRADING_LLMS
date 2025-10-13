# 📦 ARCHIVOS PARA COPIAR AL SERVIDOR

## ✅ LISTA COMPLETA DE ARCHIVOS NECESARIOS

### **Scripts Python (10 archivos)**
```
trading_bot.py
model_comparison.py
analyze_models.py
analyze_performance.py
analyze_by_period.py
quick_compare.py
manage_logs.py
```

### **Configuración (3 archivos)**
```
config.yml
.env
requirements.txt
```

### **Documentación (opcional - 7 archivos)**
```
README.md
MODEL_COMPARISON_GUIDE.md
EXAMPLE_OUTPUT.md
CONFIG_GUIDE.md
MONITORING_GUIDE.md
DEPLOYMENT_GUIDE.md
MODEL_COMPARISON_SUMMARY.md
```

---

## 🚀 COMANDO RÁPIDO PARA COPIAR

### **Copiar solo archivos esenciales:**

```powershell
# Crear carpeta temporal
mkdir deploy_package

# Copiar archivos esenciales
copy trading_bot.py deploy_package\
copy model_comparison.py deploy_package\
copy analyze_models.py deploy_package\
copy analyze_performance.py deploy_package\
copy analyze_by_period.py deploy_package\
copy quick_compare.py deploy_package\
copy manage_logs.py deploy_package\
copy config.yml deploy_package\
copy .env deploy_package\
copy requirements.txt deploy_package\
copy DEPLOYMENT_GUIDE.md deploy_package\

# Comprimir (si tienes 7-Zip instalado)
7z a -tzip TradingBot_Deploy.zip deploy_package\*

# O crear sin comprimir para USB
xcopy deploy_package\* E:\TradingBot\ /E /I
```

---

## 📋 CHECKLIST DE TRANSFERENCIA

### **Antes de transferir:**
- [ ] Verificar que `.env` tiene las 3 API keys
- [ ] Verificar que `config.yml` está configurado correctamente
- [ ] Backup de archivos CSV actuales (si quieres conservarlos)

### **En el servidor:**
- [ ] Python 3.12+ instalado
- [ ] Git instalado (opcional)
- [ ] Conexión a internet activa
- [ ] Suficiente espacio en disco (mínimo 1 GB libre)

### **Después de transferir:**
- [ ] Crear entorno virtual
- [ ] Instalar dependencias
- [ ] Probar ejecución
- [ ] Configurar inicio automático

---

## 💡 OPCIONES DE TRANSFERENCIA

### **Opción 1: USB**
1. Copiar carpeta `deploy_package` a USB
2. Conectar USB en servidor
3. Copiar carpeta a `C:\TradingBot`

### **Opción 2: Red compartida**
```powershell
# Compartir carpeta en tu PC
# En el servidor:
xcopy "\\TU_PC\deploy_package\*" "C:\TradingBot\" /E /I
```

### **Opción 3: OneDrive/Dropbox**
1. Subir `deploy_package` a la nube
2. Descargar en el servidor

### **Opción 4: Git (si ya está en GitHub)**
```powershell
# En el servidor:
git clone https://github.com/amaliogomezlopez/TRADING_LLMS.git C:\TradingBot
cd C:\TradingBot

# Crear .env manualmente (no está en GitHub)
notepad .env
```

---

## ⚠️ ARCHIVOS QUE **NO** NECESITAS COPIAR

```
.venv/                  ← Se crea nuevo en servidor
__pycache__/           ← Se genera automático
*.pyc                  ← Archivos compilados
.git/                  ← Opcional
trading_log.csv        ← Opcional (histórico)
model_comparison.csv   ← Opcional (histórico)
logs_backup/           ← Opcional (histórico)
.gitignore             ← No necesario
LICENSE                ← Opcional
```

---

## 📦 TAMAÑO APROXIMADO

```
Archivos esenciales:     ~150 KB
Con documentación:       ~250 KB
Entorno virtual (.venv): ~500 MB (se crea en servidor)
Dependencias (pandas):   ~100 MB (se descargan en servidor)
```

**Total después de instalación:** ~600 MB

---

## 🔐 SEGURIDAD DEL ARCHIVO .env

⚠️ **NUNCA compartas el archivo `.env` públicamente**

Si tranfieres por red:
- ✅ Usar conexión segura (VPN o red local)
- ✅ Eliminar archivo después de copiar
- ✅ Verificar que no queda en carpetas temporales

Si tranfieres por USB:
- ✅ Formatear USB después
- ✅ Usar USB cifrado si es posible

---

🚀 **Con estos archivos podrás desplegar el bot en cualquier servidor Windows!**
