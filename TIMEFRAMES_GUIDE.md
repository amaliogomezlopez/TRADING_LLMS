# ⏱️ GUÍA DE TIMEFRAMES - TRADING BOT

## 🎯 ¿QUÉ TIMEFRAME USAR?

### 📊 RELACIÓN: Timeframe ↔ Frecuencia de Trading

**REGLA DE ORO**: El timeframe de las velas determina cada cuánto tiempo debes analizar el mercado.

```
Timeframe = Frecuencia de análisis óptima
```

**¿Por qué?**
- Los indicadores técnicos (RSI, MACD, EMAs) se calculan sobre las velas cerradas
- Si analizas antes de que cierre la vela, estás viendo los mismos datos
- Analizar más rápido que el timeframe = **desperdicio de recursos** sin nueva info

---

## ⚡ TIMEFRAMES DISPONIBLES

### 1️⃣ **1 MINUTO - Ultra Rápido (Scalping)**

```python
INTERVAL = Client.KLINE_INTERVAL_1MINUTE
wait_time = 60  # 1 minuto
```

**Características:**
- ⏱️ **Frecuencia**: Cada 1 minuto
- 📊 **Oportunidades**: ~1,440 por día
- 💰 **Estilo**: Scalping (ganancias pequeñas, muchas operaciones)
- ⚠️ **Riesgo**: MUY ALTO
- 💸 **Comisiones**: ALTAS (muchos trades)
- 🎯 **Para**: Traders muy experimentados

**Ventajas:**
✓ Muchas oportunidades
✓ Reacción rápida a movimientos

**Desventajas:**
✗ Mucho ruido del mercado
✗ Comisiones elevadas
✗ Requiere atención constante
✗ Alto estrés

---

### 2️⃣ **5 MINUTOS - Rápido**

```python
INTERVAL = Client.KLINE_INTERVAL_5MINUTE
wait_time = 300  # 5 minutos
```

**Características:**
- ⏱️ **Frecuencia**: Cada 5 minutos
- 📊 **Oportunidades**: ~288 por día
- 💰 **Estilo**: Day trading agresivo
- ⚠️ **Riesgo**: ALTO
- 💸 **Comisiones**: Moderadas-Altas
- 🎯 **Para**: Traders activos

**Ventajas:**
✓ Buena cantidad de oportunidades
✓ Filtra algo del ruido
✓ Respuesta relativamente rápida

**Desventajas:**
✗ Todavía bastante ruido
✗ Requiere monitoreo frecuente

**👉 CONFIGURACIÓN ACTUAL DEL BOT**

---

### 3️⃣ **15 MINUTOS - Balanceado (Recomendado para Testing)**

```python
INTERVAL = Client.KLINE_INTERVAL_15MINUTE
wait_time = 900  # 15 minutos
```

**Características:**
- ⏱️ **Frecuencia**: Cada 15 minutos
- 📊 **Oportunidades**: ~96 por día
- 💰 **Estilo**: Day trading moderado
- ⚠️ **Riesgo**: MEDIO
- 💸 **Comisiones**: Moderadas
- 🎯 **Para**: Balance entre actividad y análisis

**Ventajas:**
✓ Buen balance actividad/calidad
✓ Menos ruido del mercado
✓ Comisiones razonables
✓ Bueno para testing inicial

**Desventajas:**
✗ Menos oportunidades que 5m

**👉 RECOMENDADO PARA EMPEZAR**

---

### 4️⃣ **1 HORA - Conservador**

```python
INTERVAL = Client.KLINE_INTERVAL_1HOUR
wait_time = 3600  # 1 hora
```

**Características:**
- ⏱️ **Frecuencia**: Cada 1 hora
- 📊 **Oportunidades**: ~24 por día
- 💰 **Estilo**: Position trading
- ⚠️ **Riesgo**: BAJO-MEDIO
- 💸 **Comisiones**: Bajas
- 🎯 **Para**: Traders con menos tiempo

**Ventajas:**
✓ Tendencias más claras
✓ Poco ruido
✓ No requiere atención constante
✓ Comisiones mínimas

**Desventajas:**
✗ Pocas oportunidades
✗ Movimientos más lentos

---

### 5️⃣ **4 HORAS - Muy Conservador**

```python
INTERVAL = Client.KLINE_INTERVAL_4HOUR
wait_time = 14400  # 4 horas
```

**Características:**
- ⏱️ **Frecuencia**: Cada 4 horas
- 📊 **Oportunidades**: ~6 por día
- 💰 **Estilo**: Swing trading
- ⚠️ **Riesgo**: BAJO
- 💸 **Comisiones**: Muy bajas
- 🎯 **Para**: Traders de largo plazo

**Ventajas:**
✓ Tendencias muy claras
✓ Casi sin ruido
✓ Revisión ocasional
✓ Muy bajo costo en comisiones

**Desventajas:**
✗ Muy pocas oportunidades
✗ Requiere paciencia

---

### 6️⃣ **1 DÍA - Swing Trading**

```python
INTERVAL = Client.KLINE_INTERVAL_1DAY
wait_time = 86400  # 1 día
```

**Características:**
- ⏱️ **Frecuencia**: Cada 1 día
- 📊 **Oportunidades**: ~30 por mes
- 💰 **Estilo**: Swing/Position trading
- ⚠️ **Riesgo**: MUY BAJO
- 💸 **Comisiones**: Insignificantes
- 🎯 **Para**: Inversores a largo plazo

**Ventajas:**
✓ Máxima claridad de tendencias
✓ Sin ruido
✓ Set & forget
✓ Sin estrés

**Desventajas:**
✗ Muy pocas operaciones
✗ Requiere mucha paciencia

---

## 🎯 RECOMENDACIONES POR EXPERIENCIA

### 👶 **Principiante**
```
15 minutos o 1 hora
```
- Suficientes oportunidades para aprender
- No abrumador
- Tiempo para analizar decisiones

### 👨‍💼 **Intermedio**
```
5 minutos o 15 minutos
```
- Más actividad
- Balance entre velocidad y análisis

### 🏆 **Avanzado**
```
1 minuto a 15 minutos
```
- Experiencia para manejar velocidad
- Comprensión profunda del mercado

---

## 🔧 CÓMO CAMBIAR EL TIMEFRAME

### Paso 1: Editar `trading_bot.py`

Busca estas líneas:

```python
# --- Trading Bot Parameters ---
INTERVAL = Client.KLINE_INTERVAL_5MINUTE  # ← CAMBIAR AQUÍ
```

### Paso 2: Cambiar el wait_time

Busca al final del archivo:

```python
wait_time = 300  # ← AJUSTAR SEGÚN TIMEFRAME
```

**Tabla de wait_time:**
```python
1 minuto   → wait_time = 60
5 minutos  → wait_time = 300
15 minutos → wait_time = 900
1 hora     → wait_time = 3600
4 horas    → wait_time = 14400
1 día      → wait_time = 86400
```

### Paso 3: Reiniciar el bot

```powershell
# Detener bot (Ctrl+C)
# Reiniciar
.\.venv\Scripts\Activate.ps1; python trading_bot.py
```

---

## ⚖️ COMPARACIÓN DE TIMEFRAMES

| Timeframe | Trades/Día | Riesgo | Comisiones | Atención | Recomendado |
|-----------|------------|--------|------------|----------|-------------|
| 1m        | ~1,440     | ⚠️⚠️⚠️⚠️⚠️ | 💸💸💸💸💸 | 🔴🔴🔴🔴🔴 | Expertos |
| 5m        | ~288       | ⚠️⚠️⚠️⚠️ | 💸💸💸💸 | 🔴🔴🔴🔴 | Activos |
| 15m       | ~96        | ⚠️⚠️⚠️ | 💸💸💸 | 🔴🔴🔴 | **TESTING** |
| 1h        | ~24        | ⚠️⚠️ | 💸💸 | 🔴🔴 | Casual |
| 4h        | ~6         | ⚠️ | 💸 | 🔴 | Conservador |
| 1d        | ~1         | ✅ | ✅ | ✅ | Pasivo |

---

## 💡 CONSEJOS PRO

### 1. **Empezar Lento**
- Comienza con 15 minutos o 1 hora
- Cuando domines, baja a 5 minutos
- Solo expertos deberían usar 1 minuto

### 2. **Ajustar Stop Loss según Timeframe**
```python
# Timeframes cortos = Stop loss más ajustado
1 minuto  → STOP_LOSS_PERCENT = 0.005  # 0.5%
5 minutos → STOP_LOSS_PERCENT = 0.01   # 1%
15 minutos → STOP_LOSS_PERCENT = 0.02  # 2%
1 hora    → STOP_LOSS_PERCENT = 0.03   # 3%
```

### 3. **Más Rápido ≠ Más Ganancias**
- Timeframes cortos tienen más ruido
- Más trades = más comisiones
- Calidad > Cantidad

### 4. **Testing por Timeframe**
Testa cada timeframe al menos:
- 1 minuto: 4-8 horas
- 5 minutos: 24 horas
- 15 minutos: 48 horas
- 1 hora: 1 semana

---

## 🎬 CONFIGURACIÓN ACTUAL

**Tu bot está configurado para:**
```
⏱️ Timeframe: 5 MINUTOS
📊 Ciclo cada: 5 minutos
💰 Estilo: Day trading rápido
⚠️ Riesgo: Alto
```

---

## 🔄 CAMBIAR A DIFERENTES ESTRATEGIAS

### 📈 **Estrategia Agresiva (Scalping)**
```python
INTERVAL = Client.KLINE_INTERVAL_1MINUTE
wait_time = 60
STOP_LOSS_PERCENT = 0.005  # 0.5%
TAKE_PROFIT_PERCENT = 0.01  # 1%
```

### ⚖️ **Estrategia Balanceada**
```python
INTERVAL = Client.KLINE_INTERVAL_15MINUTE
wait_time = 900
STOP_LOSS_PERCENT = 0.02  # 2%
TAKE_PROFIT_PERCENT = 0.03  # 3%
```

### 🛡️ **Estrategia Conservadora**
```python
INTERVAL = Client.KLINE_INTERVAL_1HOUR
wait_time = 3600
STOP_LOSS_PERCENT = 0.03  # 3%
TAKE_PROFIT_PERCENT = 0.05  # 5%
```

---

## ✅ RESUMEN

**PREGUNTA**: ¿Por qué no más rápido?

**RESPUESTA**: 
- Los datos solo cambian cuando cierra la vela
- Analizar antes = ver los mismos datos
- **Timeframe de vela = Frecuencia óptima**

**SOLUCIÓN**: 
- Cambia el INTERVAL a un timeframe más corto
- Ajusta el wait_time correspondientemente
- **5 minutos es un buen balance para empezar** ✓

---

¡Ahora el bot analizará cada 5 minutos! 🚀
