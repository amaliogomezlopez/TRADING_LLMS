# 📊 GUÍA DE MONITOREO - Trading Bot

## 🎯 Respuesta Rápida

### ❌ **NO es necesario borrar el log**

El archivo `trading_log.csv` es **acumulativo** y eso es **beneficioso**:
- ✅ Mantiene historial completo
- ✅ Permite comparar períodos
- ✅ Analiza evolución de la estrategia
- ✅ Identifica patrones

---

## 📈 ESTRATEGIAS DE MONITOREO

### 1️⃣ **Monitoreo Continuo (RECOMENDADO)**

Deja el log acumulándose y analiza por períodos.

**Ventajas:**
- Historial completo
- Comparación temporal
- Análisis de mejoras

**Cómo hacerlo:**

```powershell
# Analizar las últimas 2 horas
.\.venv\Scripts\Activate.ps1; python analyze_by_period.py 2

# Analizar las últimas 4 horas
.\.venv\Scripts\Activate.ps1; python analyze_by_period.py 4

# Analizar todo el período
.\.venv\Scripts\Activate.ps1; python analyze_performance.py
```

---

### 2️⃣ **Nuevo Ciclo con Backup**

Si quieres "empezar limpio" pero mantener historial.

```powershell
# Hacer backup y limpiar log
.\.venv\Scripts\Activate.ps1; python manage_logs.py clean
```

**Qué hace:**
1. ✅ Crea backup con timestamp
2. ✅ Guarda en `logs_backup/`
3. ✅ Limpia el log actual
4. ✅ El bot empieza con log limpio

---

### 3️⃣ **Borrado Manual** (NO recomendado)

Si **realmente** quieres empezar de cero:

```powershell
# Ver info actual
.\.venv\Scripts\Activate.ps1; python manage_logs.py info

# Backup manual
Copy-Item trading_log.csv "trading_log_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv"

# Borrar (el bot creará uno nuevo)
Remove-Item trading_log.csv
```

---

## 🛠️ HERRAMIENTAS DE MONITOREO

### 📊 **analyze_performance.py**
Análisis completo de todo el período

```powershell
.\.venv\Scripts\Activate.ps1; python analyze_performance.py
```

**Muestra:**
- Total de ciclos
- Distribución de señales
- Win rate
- P&L total
- Métricas de riesgo

---

### ⏱️ **analyze_by_period.py** (NUEVO)
Análisis filtrado por tiempo

```powershell
# Últimas 1 hora
.\.venv\Scripts\Activate.ps1; python analyze_by_period.py 1

# Últimas 2 horas
.\.venv\Scripts\Activate.ps1; python analyze_by_period.py 2

# Últimas 8 horas
.\.venv\Scripts\Activate.ps1; python analyze_by_period.py 8

# Sin argumentos: análisis completo + comparación
.\.venv\Scripts\Activate.ps1; python analyze_by_period.py
```

**Muestra:**
- Análisis del período específico
- Comparación entre períodos
- Performance temporal

---

### 🗂️ **manage_logs.py** (NUEVO)
Gestión completa de logs

```powershell
# Ver info del log actual
.\.venv\Scripts\Activate.ps1; python manage_logs.py info

# Crear backup
.\.venv\Scripts\Activate.ps1; python manage_logs.py backup

# Backup y limpiar
.\.venv\Scripts\Activate.ps1; python manage_logs.py clean

# Listar backups
.\.venv\Scripts\Activate.ps1; python manage_logs.py list

# Menú interactivo
.\.venv\Scripts\Activate.ps1; python manage_logs.py
```

---

## 📅 PLAN DE MONITOREO RECOMENDADO

### **Día 1: Testing Inicial (2-4 horas)**

```powershell
# Hora 0: Iniciar bot
.\.venv\Scripts\Activate.ps1; python trading_bot.py

# Cada hora: Revisar últimas 2 horas
.\.venv\Scripts\Activate.ps1; python analyze_by_period.py 2

# Después de 4 horas: Análisis completo
.\.venv\Scripts\Activate.ps1; python analyze_performance.py
```

---

### **Día 2-7: Testing Extendido**

```powershell
# Mañana (revisar noche)
.\.venv\Scripts\Activate.ps1; python analyze_by_period.py 8

# Mediodía (revisar mañana)
.\.venv\Scripts\Activate.ps1; python analyze_by_period.py 4

# Noche (análisis completo del día)
.\.venv\Scripts\Activate.ps1; python analyze_performance.py
```

---

### **Cada semana: Backup y Análisis**

```powershell
# Crear backup semanal
.\.venv\Scripts\Activate.ps1; python manage_logs.py backup

# Análisis completo
.\.venv\Scripts\Activate.ps1; python analyze_performance.py

# Opcional: Empezar nueva semana limpio
.\.venv\Scripts\Activate.ps1; python manage_logs.py clean
```

---

## 🎨 EJEMPLOS DE USO

### Ejemplo 1: Monitoreo cada 2 horas

```powershell
# Ejecutar este comando cada 2 horas
while ($true) {
    Clear-Host
    .\.venv\Scripts\Activate.ps1
    python analyze_by_period.py 2
    Start-Sleep -Seconds 7200  # 2 horas
}
```

---

### Ejemplo 2: Ver log en tiempo real

```powershell
# Ver últimas 10 líneas actualizándose
while ($true) {
    Clear-Host
    Get-Content trading_log.csv -Tail 10
    Start-Sleep -Seconds 60
}
```

---

### Ejemplo 3: Dashboard simple

```powershell
# Script de monitoreo
while ($true) {
    Clear-Host
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host "🤖 TRADING BOT DASHBOARD" -ForegroundColor Cyan
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Info del log
    .\.venv\Scripts\Activate.ps1
    python manage_logs.py info
    
    Write-Host ""
    Write-Host "Última actualización: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Yellow
    Write-Host "Próxima actualización en 5 minutos..." -ForegroundColor Gray
    
    Start-Sleep -Seconds 300
}
```

---

## 📦 ESTRUCTURA DE BACKUPS

Después de usar `manage_logs.py`, tendrás:

```
24-TRADING_AI/
├── trading_log.csv          ← Log actual (activo)
├── logs_backup/             ← Backups automáticos
│   ├── trading_log_20251013_120000.csv
│   ├── trading_log_20251013_180000.csv
│   └── trading_log_20251014_090000.csv
├── analyze_performance.py
├── analyze_by_period.py
└── manage_logs.py
```

---

## 🔍 COMPARACIÓN DE MÉTODOS

### Método 1: Análisis por Período (SIN borrar)

```powershell
# ✅ VENTAJAS:
- Historial completo
- Comparar períodos
- Sin pérdida de datos
- Análisis temporal

# ❌ DESVENTAJAS:
- Archivo crece con el tiempo
- Más datos para procesar
```

**RECOMENDADO PARA:** Testing de largo plazo, análisis profundo

---

### Método 2: Backup y Limpiar

```powershell
# ✅ VENTAJAS:
- Archivo más pequeño
- Fácil ver resultados recientes
- Organizaci ón por períodos

# ❌ DESVENTAJAS:
- Requiere gestión manual
- Múltiples archivos
```

**RECOMENDADO PARA:** Testear cambios de configuración, ciclos semanales

---

### Método 3: Borrar sin Backup

```powershell
# ✅ VENTAJAS:
- Empezar "limpio"

# ❌❌❌ DESVENTAJAS:
- Pérdida de datos
- No hay historial
- No se puede comparar
```

**❌ NO RECOMENDADO**

---

## 📊 MÉTRICAS CLAVE A MONITOREAR

### Cada Hora:
- [ ] Total de ciclos ejecutados
- [ ] Señales generadas (BUY/SELL/HOLD)
- [ ] Trades abiertos vs cerrados
- [ ] Errores o warnings

### Cada 4 Horas:
- [ ] Win rate
- [ ] P&L del período
- [ ] RSI promedio
- [ ] Distribución de señales

### Cada Día:
- [ ] P&L total
- [ ] Profit factor
- [ ] Máximas ganancias/pérdidas
- [ ] Comparación con día anterior

### Cada Semana:
- [ ] Backup del log
- [ ] Análisis completo
- [ ] Optimización de parámetros
- [ ] Ajustes de estrategia

---

## 🎯 RECOMENDACIÓN FINAL

### Para tu caso:

```powershell
# 1. NO BORRES el log actual
# 2. Deja el bot corriendo 4-8 horas
# 3. Analiza por períodos cada 2 horas:

.\.venv\Scripts\Activate.ps1; python analyze_by_period.py 2

# 4. Al final del día, análisis completo:

.\.venv\Scripts\Activate.ps1; python analyze_performance.py

# 5. Si quieres empezar "limpio" mañana:

.\.venv\Scripts\Activate.ps1; python manage_logs.py clean
```

---

## 🚀 COMANDOS RÁPIDOS

```powershell
# Ver info del log
python manage_logs.py info

# Análisis últimas 2 horas
python analyze_by_period.py 2

# Análisis completo
python analyze_performance.py

# Crear backup
python manage_logs.py backup

# Backup y limpiar
python manage_logs.py clean

# Ver últimas líneas del log
Get-Content trading_log.csv -Tail 20
```

---

## ✅ RESUMEN

| Acción | Comando | Cuándo Usar |
|--------|---------|-------------|
| **Análisis período** | `python analyze_by_period.py 2` | Cada 2 horas |
| **Análisis completo** | `python analyze_performance.py` | Cada día |
| **Ver log actual** | `python manage_logs.py info` | Cuando quieras |
| **Crear backup** | `python manage_logs.py backup` | Cada semana |
| **Limpiar log** | `python manage_logs.py clean` | Nuevos ciclos |

**NO ES NECESARIO BORRAR EL LOG** - Usa las herramientas de análisis por período! 📊
