# ⚙️ SISTEMA DE CONFIGURACIÓN - Trading Bot

## 🎯 ¿Qué es esto?

Un sistema de configuración **centralizado** con archivo YAML que te permite cambiar **todos los parámetros del bot** sin tocar el código.

---

## 📁 Archivos de Configuración

### `config.yml` 
**Tu configuración personalizada** (editaste aquí)

### `config.example.yml`
**Plantilla de ejemplo** (para referencia o restaurar)

---

## ✨ Ventajas del Sistema

### ✅ **ANTES** (Sin YAML)
```python
# Tenías que editar el código Python directamente
INTERVAL = Client.KLINE_INTERVAL_5MINUTE  # ← Buscar esta línea
STOP_LOSS_PERCENT = 0.02                  # ← Buscar esta otra
RSI_OVERSOLD = 30                         # ← Y esta...
```

❌ Complicado
❌ Fácil de romper
❌ Difícil de versionar

### ✅ **AHORA** (Con YAML)
```yaml
# Editas un archivo simple y limpio
trading:
  timeframe: '5m'        # ← Cambias aquí
risk_management:
  stop_loss_percent: 0.02  # ← Y aquí
technical_indicators:
  rsi:
    oversold: 30         # ← Y aquí
```

✅ Simple
✅ Seguro
✅ Fácil de respaldar

---

## 🚀 Cómo Usar

### 1. **Editar Configuración**

Abre `config.yml` y modifica lo que necesites:

```yaml
trading:
  timeframe: '15m'   # Cambiar de 5m a 15m
```

### 2. **Guardar Cambios**

Simplemente guarda el archivo (Ctrl+S)

### 3. **Reiniciar el Bot**

```powershell
# Detener el bot actual (Ctrl+C)
# Reiniciar
.\.venv\Scripts\Activate.ps1; python trading_bot.py
```

El bot cargará automáticamente la nueva configuración:
```
✓ Configuration loaded from config.yml
```

---

## 📊 Parámetros Configurables

### 🎯 **Trading**

```yaml
trading:
  symbol: 'BTCUSDT'      # Par de trading
  quantity: 0.001        # Cantidad por operación
  timeframe: '5m'        # Velocidad del bot
```

**Timeframes disponibles:**
- `'1m'` = 1 minuto (ultra rápido)
- `'5m'` = 5 minutos (rápido) ← **ACTUAL**
- `'15m'` = 15 minutos (balanceado)
- `'1h'` = 1 hora (conservador)
- `'4h'` = 4 horas (muy conservador)
- `'1d'` = 1 día (swing trading)

---

### 🛡️ **Gestión de Riesgo**

```yaml
risk_management:
  stop_loss_percent: 0.02      # 2%
  take_profit_percent: 0.03    # 3%
  max_total_loss: -100.0       # $100
```

**Ejemplos de ajuste:**

**Más conservador:**
```yaml
stop_loss_percent: 0.015       # 1.5% (más ajustado)
take_profit_percent: 0.04      # 4% (objetivo mayor)
max_total_loss: -50.0          # $50 (más cauteloso)
```

**Más agresivo:**
```yaml
stop_loss_percent: 0.03        # 3% (más espacio)
take_profit_percent: 0.02      # 2% (objetivo menor, más rápido)
max_total_loss: -200.0         # $200 (más tolerante)
```

---

### 📈 **Indicadores Técnicos**

```yaml
technical_indicators:
  rsi:
    period: 14           # Período de cálculo
    oversold: 30         # Umbral de sobreventa
    overbought: 70       # Umbral de sobrecompra
  
  ema:
    short_period: 9      # EMA rápida
    long_period: 21      # EMA lenta
  
  klines_limit: 100      # Velas para análisis
```

**Ajustes comunes:**

**RSI más sensible:**
```yaml
rsi:
  oversold: 35    # Más operaciones de compra
  overbought: 65  # Más operaciones de venta
```

**EMAs más rápidas:**
```yaml
ema:
  short_period: 5    # Más reactivo
  long_period: 13    # Más señales
```

---

### 🤖 **LLM (Groq)**

```yaml
llm:
  model: 'llama-3.1-8b-instant'
  temperature: 0.3
  max_tokens: 20
```

**Temperature:**
- `0.0` - `0.2`: Muy conservador, consistente
- `0.3` - `0.5`: Balanceado ← **ACTUAL**
- `0.6` - `1.0`: Más creativo, variable

---

### 📝 **Logging**

```yaml
logging:
  log_file: 'trading_log.csv'
  enable_console_output: true
```

---

## 🎨 Ejemplos de Configuraciones

### 🏃 **Scalping Agresivo (1 minuto)**

```yaml
trading:
  timeframe: '1m'
  quantity: 0.001

risk_management:
  stop_loss_percent: 0.005    # 0.5%
  take_profit_percent: 0.01   # 1%
  max_total_loss: -50.0

technical_indicators:
  rsi:
    oversold: 25
    overbought: 75

llm:
  temperature: 0.2   # Más consistente
```

---

### ⚖️ **Day Trading Balanceado (15 minutos)**

```yaml
trading:
  timeframe: '15m'
  quantity: 0.001

risk_management:
  stop_loss_percent: 0.02     # 2%
  take_profit_percent: 0.03   # 3%
  max_total_loss: -100.0

technical_indicators:
  rsi:
    oversold: 30
    overbought: 70

llm:
  temperature: 0.3   # Balanceado
```

---

### 🛡️ **Swing Trading Conservador (4 horas)**

```yaml
trading:
  timeframe: '4h'
  quantity: 0.002    # Más cantidad, menos trades

risk_management:
  stop_loss_percent: 0.04     # 4%
  take_profit_percent: 0.06   # 6%
  max_total_loss: -200.0

technical_indicators:
  rsi:
    oversold: 35
    overbought: 65
  ema:
    short_period: 13
    long_period: 34

llm:
  temperature: 0.4   # Más flexible
```

---

## 🔄 Cambiar Timeframe Rápido

### Para cambiar la velocidad del bot:

**1. Abrir `config.yml`**

**2. Cambiar una sola línea:**
```yaml
timeframe: '15m'   # De 5m a 15m
```

**3. Reiniciar bot**

¡Eso es todo! El bot automáticamente:
- ✅ Cambia el intervalo de velas
- ✅ Ajusta el tiempo de espera
- ✅ Sincroniza todo correctamente

---

## 🎯 Flujo de Trabajo Recomendado

### 1. **Testing Inicial**
```yaml
timeframe: '15m'   # Empezar lento
max_total_loss: -50.0
```

### 2. **Después de 24h de Testing**
Si funciona bien:
```yaml
timeframe: '5m'    # Aumentar velocidad
max_total_loss: -100.0
```

### 3. **Optimización**
Ajustar según resultados:
```yaml
stop_loss_percent: 0.015  # Si hay muchas pérdidas
take_profit_percent: 0.04  # Si se sale muy pronto
```

---

## 🛠️ Troubleshooting

### ⚠️ Error: "Configuration file not found"

**Solución 1:** Renombrar archivo
```powershell
Copy-Item config.example.yml config.yml
```

**Solución 2:** El bot usará valores por defecto
```
⚠️ Configuration file config.yml not found. Using default values.
```

---

### ⚠️ Error al cargar YAML

**Verifica la sintaxis:**
- Usa espacios, NO tabs
- Respeta la indentación
- Comillas en strings: `'5m'` no `5m`

**Formato correcto:**
```yaml
trading:           # Sin espacios antes
  symbol: 'BTCUSDT'    # 2 espacios de indentación
  timeframe: '5m'      # Comillas en el valor
```

---

## 📦 Backup de Configuración

### Crear respaldo:
```powershell
Copy-Item config.yml "config_backup_$(Get-Date -Format 'yyyyMMdd').yml"
```

### Restaurar:
```powershell
Copy-Item config.example.yml config.yml
```

---

## 🎓 Tips Pro

### 1. **Versionar Configuraciones**

Crea múltiples configs para diferentes estrategias:
```
config_scalping.yml
config_daytrading.yml
config_conservative.yml
```

Usar una específica:
```python
config = load_config('config_scalping.yml')
```

### 2. **Comentar Cambios**

```yaml
trading:
  timeframe: '5m'   # Cambiado de 15m (2025-10-13)
```

### 3. **Testing A/B**

Prueba 2 configuraciones en paralelo y compara resultados.

---

## ✅ Ventajas del Sistema

| Antes (Sin YAML) | Ahora (Con YAML) |
|------------------|------------------|
| Editar código Python | Editar archivo simple |
| Buscar variables | Todo centralizado |
| Riesgo de bugs | Seguro |
| Difícil de compartir | Fácil de exportar |
| Un archivo | Múltiples configs |

---

## 🎉 ¡Listo!

Ahora puedes **cambiar cualquier parámetro del bot** editando solo `config.yml` sin tocar el código.

**Cambios comunes:**
- ⏱️ **Timeframe**: `timeframe: '15m'`
- 🛡️ **Stop Loss**: `stop_loss_percent: 0.015`
- 🎯 **Take Profit**: `take_profit_percent: 0.04`
- 📊 **RSI**: `oversold: 35`

**Reiniciar bot → ¡Nueva configuración aplicada!** 🚀
