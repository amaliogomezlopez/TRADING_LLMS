# 🧪 PLAN DE TESTING DEL TRADING BOT

## 📋 Estrategia de Testing Recomendada

### ✅ Fase 1: Testing Corto (2-4 horas)
**Objetivo**: Verificar que todo funciona correctamente

### ✅ Fase 2: Testing Medio (24-48 horas)
**Objetivo**: Evaluar performance y ajustar parámetros

### ✅ Fase 3: Testing Extendido (1 semana)
**Objetivo**: Validar estrategia antes de considerar dinero real

---

## 🚀 CÓMO INICIAR EL BOT

### 1. Preparación

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Verificar que las dependencias están instaladas
pip list | Select-String "binance|groq|ta|pandas"

# Verificar que .env está configurado
Get-Content .env
```

### 2. Limpiar Logs Anteriores (Opcional)

```powershell
# Hacer backup del log anterior
if (Test-Path trading_log.csv) {
    Copy-Item trading_log.csv "trading_log_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv"
    Remove-Item trading_log.csv
}
```

### 3. Ejecutar el Bot

```powershell
python trading_bot.py
```

**El bot mostrará:**
```
============================================================
ADVANCED TRADING BOT WITH TECHNICAL ANALYSIS
============================================================
Symbol: BTCUSDT
Interval: 15m
Stop Loss: 2.0%
Take Profit: 3.0%
Max Total Loss: $-100.0
============================================================
Successfully connected to Binance Testnet.

============================================================
CYCLE #1 - 2025-10-13 14:30:00
============================================================
✓ Market data fetched: 100 candles

📊 TECHNICAL ANALYSIS:
   Price: $62,450 (+2.5%)
   RSI: 45 - NEUTRAL
   MACD: BULLISH (Above signal line)
   Trend: BULLISH (short) / BULLISH (medium)
   EMA: Price is ABOVE EMA9, ABOVE EMA21

🤖 LLM DECISION: BUY

✅ BUY EXECUTED at $62,450.00
   Stop Loss: $61,201.00
   Take Profit: $64,323.50

⏳ Waiting 15 minutes for next cycle...
```

---

## ⏱️ TESTING SCHEDULE

### 🔴 Testing Corto (2-4 horas) - RECOMENDADO PARA EMPEZAR

**Duración**: 8-16 ciclos (cada ciclo = 15 minutos)

**Objetivo**: Verificar funcionamiento básico

**Qué observar**:
- ✅ Bot se conecta a Binance
- ✅ Datos técnicos se calculan correctamente
- ✅ LLM responde con decisiones válidas
- ✅ Logs se generan correctamente
- ✅ No hay errores de ejecución

**Comando**:
```powershell
# Ejecutar por 2 horas (8 ciclos)
python trading_bot.py
# Presiona Ctrl+C después de 2-4 horas
```

---

### 🟡 Testing Medio (24-48 horas)

**Duración**: 96-192 ciclos

**Objetivo**: Evaluar toma de decisiones

**Qué observar**:
- 📊 Distribución de señales (BUY/SELL/HOLD)
- 💰 Performance (win rate, P&L)
- 🛡️ Funcionamiento de stop loss/take profit
- 📈 Calidad de las entradas/salidas

**Ejecución en Background** (Windows):
```powershell
# Opción 1: En PowerShell sin cerrar
python trading_bot.py

# Opción 2: Con nohup (Git Bash)
nohup python trading_bot.py > output.log 2>&1 &

# Opción 3: Como tarea programada
# Ver más abajo la sección "Ejecutar en Background"
```

---

### 🟢 Testing Extendido (1 semana)

**Duración**: ~672 ciclos (1 semana)

**Objetivo**: Validación completa de estrategia

**Qué observar**:
- 📊 Profit Factor > 1.5
- 🎯 Win Rate > 50%
- 💵 P&L consistente
- 🔄 Comportamiento en diferentes condiciones de mercado

---

## 📊 MONITOREO DURANTE EL TESTING

### 1. Ver el Log en Tiempo Real

Abre una **segunda terminal** y ejecuta:

```powershell
# Ver últimas líneas del log
Get-Content trading_log.csv -Tail 10

# Ver log en tiempo real (actualiza cada 5 segundos)
while ($true) {
    Clear-Host
    Get-Content trading_log.csv -Tail 20
    Start-Sleep -Seconds 5
}
```

### 2. Análisis Periódico

Cada hora, ejecuta el análisis:

```powershell
python analyze_performance.py
```

**Salida esperada**:
```
============================================================
📊 ANÁLISIS DEL TRADING BOT
============================================================

📅 PERÍODO:
   Total de ciclos: 32

🤖 SEÑALES DEL LLM:
   BUY: 8 (25.0%)
   SELL: 6 (18.8%)
   HOLD: 18 (56.2%)

💰 TRADES:
   Compras (BUY): 8
   Ventas (SELL): 6

📈 PERFORMANCE:
   Win Rate: 66.7%
   Total P&L: $12.50
```

### 3. Monitoreo de Recursos

```powershell
# Ver uso de CPU y memoria del proceso Python
Get-Process python | Select-Object CPU, PM, WS
```

---

## 🖥️ EJECUTAR EN BACKGROUND (Windows)

### Opción A: PowerShell sin cerrar la ventana

```powershell
# Simplemente deja la terminal abierta minimizada
python trading_bot.py
```

### Opción B: Con Start-Process (PowerShell)

```powershell
# Inicia en nueva ventana
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\.venv\Scripts\Activate.ps1; python trading_bot.py"
```

### Opción C: Tarea Programada de Windows

1. **Crear script de inicio** (`start_bot.ps1`):
```powershell
cd "C:\Users\amalio\Desktop\PROGRAMACION\01-VS_CODE\24-TRADING_AI"
.\.venv\Scripts\Activate.ps1
python trading_bot.py
```

2. **Programar en Task Scheduler**:
```powershell
# Abrir Task Scheduler
taskschd.msc

# O crear desde PowerShell (como Admin)
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\Users\amalio\Desktop\PROGRAMACION\01-VS_CODE\24-TRADING_AI\start_bot.ps1"
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -TaskName "TradingBot" -Action $action -Trigger $trigger
```

### Opción D: Con Python Daemon (Mejor para 24/7)

Crea `run_bot_daemon.py`:
```python
import subprocess
import time
from datetime import datetime

def run_bot():
    while True:
        print(f"[{datetime.now()}] Iniciando bot...")
        try:
            subprocess.run(["python", "trading_bot.py"])
        except Exception as e:
            print(f"Error: {e}")
            print("Reiniciando en 60 segundos...")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()
```

---

## 🎯 CHECKLIST DE TESTING

### Antes de Iniciar
- [ ] `.env` configurado con API keys correctas
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas
- [ ] Binance Testnet accesible
- [ ] Groq API funcionando

### Durante el Testing (cada hora)
- [ ] Bot sigue ejecutando sin errores
- [ ] Logs se están generando
- [ ] Decisiones del LLM son razonables
- [ ] Stop Loss/Take Profit funcionan
- [ ] No hay errores de API

### Después del Testing
- [ ] Ejecutar `analyze_performance.py`
- [ ] Revisar win rate y P&L
- [ ] Identificar patrones en las decisiones
- [ ] Ajustar parámetros si es necesario

---

## 📈 ANÁLISIS POST-TESTING

### 1. Ejecutar Análisis Completo

```powershell
python analyze_performance.py
```

### 2. Revisar el CSV Manualmente

```powershell
# Abrir en Excel
Invoke-Item trading_log.csv

# O ver en terminal
Import-Csv trading_log.csv | Format-Table -AutoSize
```

### 3. Métricas Clave a Evaluar

**✅ BUENAS SEÑALES:**
- Win Rate > 50%
- Profit Factor > 1.5
- P&L positivo
- Stop losses funcionando
- Distribución equilibrada de señales

**⚠️ SEÑALES DE ALERTA:**
- Win Rate < 40%
- P&L consistentemente negativo
- Todas las señales son iguales (ej: 100% SELL)
- Muchos trades con stop loss
- Errores de API frecuentes

---

## 🔧 AJUSTES COMUNES POST-TESTING

### Si el bot es muy conservador (muchos HOLD)

```python
# En trading_bot.py, ajusta:
RSI_OVERSOLD = 35  # Era 30
RSI_OVERBOUGHT = 65  # Era 70
```

### Si hay demasiadas pérdidas

```python
# Aumentar stop loss / reducir take profit
STOP_LOSS_PERCENT = 0.015  # 1.5% (era 2%)
TAKE_PROFIT_PERCENT = 0.04  # 4% (era 3%)
```

### Si el LLM es muy agresivo

```python
# En get_trading_signal_with_groq():
temperature=0.2,  # Reducir (era 0.3)
```

---

## 🛑 CÓMO DETENER EL BOT

### Detención Normal
```
Presiona: Ctrl + C en la terminal
```

### Detención Forzada
```powershell
# Encontrar el proceso
Get-Process python

# Matar el proceso
Stop-Process -Name python
```

### Ver si está ejecutando
```powershell
Get-Process python -ErrorAction SilentlyContinue
```

---

## 📊 REPORTE FINAL

Después de cada fase de testing, crea un reporte:

### Template de Reporte

```
TESTING REPORT - [Fecha]
========================

CONFIGURACIÓN:
- Duración: [X horas/días]
- Ciclos completados: [X]
- Symbol: BTCUSDT
- Interval: 15m

RESULTADOS:
- Total Trades: [X]
- Win Rate: [X%]
- Total P&L: $[X]
- Profit Factor: [X]

SEÑALES LLM:
- BUY: [X%]
- SELL: [X%]
- HOLD: [X%]

OBSERVACIONES:
- [Comentarios sobre el comportamiento]

AJUSTES RECOMENDADOS:
- [Si aplican]
```

---

## 🚀 RECOMENDACIÓN INICIAL

**Para tu primer test**, te sugiero:

1. **2 horas de observación activa**
   - Deja el bot corriendo
   - Observa la terminal
   - Verifica que todo funciona

2. **Después, análisis**
   ```powershell
   python analyze_performance.py
   ```

3. **Si todo va bien, 24 horas**
   - Ejecuta en background
   - Revisa cada 4-6 horas

4. **Evaluación final**
   - Analiza métricas
   - Ajusta parámetros
   - Decide si continuar

---

## ✅ COMANDO PARA EMPEZAR AHORA

```powershell
# 1. Activar entorno
.\.venv\Scripts\Activate.ps1

# 2. Iniciar bot
python trading_bot.py

# El bot comenzará a operar!
```

**¡Déjalo correr y observa!** 👀

---

¿Quieres que iniciemos el testing ahora? 🚀
