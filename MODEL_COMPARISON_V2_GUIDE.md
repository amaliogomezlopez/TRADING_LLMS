# 🚀 MODEL COMPARISON V2 - OPTIMIZED TRADING SYSTEM

## 📋 Descripción

Versión mejorada y optimizada del sistema de comparación de modelos LLM para trading. Incluye **4 modelos nuevos** (diferentes a V1) con gestión de riesgo avanzada y contexto extendido para los LLMs.

---

## 🤖 Modelos Seleccionados (V2)

| Modelo | Parámetros | Descripción | ¿Por qué? |
|--------|------------|-------------|-----------|
| **Qwen3-32B** | 32B | Ganador de V1 - Prudente | Demostró no perder dinero siendo conservador |
| **Llama-4-Maverick-17B** | 17B | Llama 4 Maverick | Variante diferente al Scout (128e vs 16e) |
| **GPT-OSS-120B** | 120B | Modelo más grande | Mayor capacidad de razonamiento |
| **Kimi-K2-Instruct** | MoonShot AI | Arquitectura china alternativa | Diversidad de perspectivas |

---

## ✨ Mejoras Implementadas

### 1️⃣ **Gestión de Riesgo Avanzada**
```python
STOP_LOSS_PERCENT = 0.02      # 2% stop loss
TAKE_PROFIT_PERCENT = 0.04    # 4% take profit (R/R 1:2)
TRAILING_STOP_PERCENT = 0.015 # 1.5% trailing stop
CONFIDENCE_THRESHOLD = 75     # Min 75% para operar
```

### 2️⃣ **Indicadores Técnicos Adicionales**
- ✅ **Stochastic Oscillator** - Momentum adicional
- ✅ **ADX** - Fuerza de la tendencia
- ✅ **ATR** - Volatilidad del mercado
- ✅ **OBV** - Análisis de volumen acumulativo
- ✅ **3 EMAs** (9, 21, 50) - Análisis multi-timeframe

### 3️⃣ **Contexto Extendido para LLMs**

El prompt ahora incluye **8 secciones** de análisis:

1. **Market Data** - Precio, volumen, cambios
2. **Trend Indicators** - EMAs, alineación, tendencias
3. **Momentum Indicators** - RSI, Stochastic, MACD
4. **Volatility** - Bollinger Bands, ATR
5. **Volume Analysis** - Ratio, OBV, confirmación
6. **Risk Assessment** - Nivel de riesgo, volatilidad
7. **Trade Setup Quality** - Score 0-10, confluencia
8. **Critical Analysis** - Reglas de decisión claras

### 4️⃣ **Sistema de Puntuación (Setup Score)**

Evalúa la calidad del setup de trading (0-10 puntos):
- **3 puntos**: Alineación perfecta de tendencias
- **2 puntos**: Confirmación RSI
- **2 puntos**: Confirmación MACD
- **2 puntos**: Confirmación de volumen
- **1 punto**: ADX fuerte (>25)

### 5️⃣ **Confianza de Consenso**

```python
confidence_score = (agreement_level * 0.7) + (setup_score * 10 * 0.3)
```

Solo opera si `confidence_score >= 75%`

### 6️⃣ **CSV Mejorado**

Nuevas columnas en `model_comparison_v2.csv`:
- `Stochastic` - Segundo indicador de momentum
- `ADX` - Fuerza de tendencia
- `Volume_Ratio` - Volumen actual vs promedio
- `Volatility` - Nivel de volatilidad
- `Setup_Score` - Calidad del setup (0-10)
- `Confidence_Score` - Confianza del consenso
- `Stop_Loss` - Precio de stop loss
- `Take_Profit` - Precio de take profit
- `Risk_Reward_Ratio` - Ratio riesgo/beneficio

---

## 🎯 Diferencias vs V1

| Característica | V1 | V2 |
|----------------|----|----|
| **Modelos** | Llama 3.3-70B, 3.1-8B, 4-Scout, Qwen | Qwen, 4-Maverick, GPT-OSS-120B, Kimi-K2 |
| **Indicadores** | 6 básicos | 12 avanzados |
| **Stop Loss** | ❌ No | ✅ Sí (2%) |
| **Take Profit** | ❌ No | ✅ Sí (4%) |
| **Setup Score** | ❌ No | ✅ Sí (0-10) |
| **Confidence** | ❌ No | ✅ Sí (0-100) |
| **Contexto Prompt** | ~300 palabras | ~600 palabras |
| **Risk/Reward** | ❌ No calculado | ✅ 1:2 |
| **Volumen OBV** | ❌ No | ✅ Sí |
| **ADX Trend** | ❌ No | ✅ Sí |
| **Threshold** | Opera siempre | Solo si confidence ≥75% |

---

## 🚀 Cómo Ejecutar

### 1. **Instalación de Dependencias**

Si no las tienes instaladas:
```bash
pip install ta pandas numpy
```

### 2. **Ejecutar el Bot**

```bash
python model_comparison_v2.py
```

### 3. **Resultados**

Se generará el archivo: `model_comparison_v2.csv`

---

## 📊 Salida de Consola

```
================================================================================
[BOT] TRADING BOT - MODEL COMPARISON V2 (OPTIMIZED)
================================================================================

[INFO] Testing 4 NEW models:
  1. Qwen3-32B: 32B params - Prudent winner from V1
  2. Llama-4-Maverick-17B: 17B params - Llama 4 Maverick variant
  3. GPT-OSS-120B: 120B params - Largest available model
  4. Kimi-K2: MoonShot AI - Alternative architecture

[CONFIG] Trading Setup:
  Symbol: BTCUSDT
  Timeframe: 5m
  Stop Loss: 2.0%
  Take Profit: 4.0%
  Risk/Reward: 1:2.0
  Confidence Threshold: 75%
  Results: model_comparison_v2.csv
================================================================================

[CYCLE] #1 - 2025-10-19 10:30:00
================================================================================

[DATA] MARKET SNAPSHOT:
  Price: $95603.10 (+0.50%)
  Trend: BULLISH / BULLISH / NEUTRAL
  RSI: 58.23 - Bullish Territory
  ADX: 32.45 - STRONG Trend
  Volume: 1.45x avg - INCREASING - Growing Interest
  Volatility: MODERATE - NORMAL RISK
  Setup Quality: 8/10 (4 indicators)

[RISK] Risk Management:
  Stop Loss: $93691.04 (-2.0%)
  Take Profit: $99427.22 (+4.0%)
  R/R Ratio: 1:2.0

[MODELS] Querying 4 models...
Model                     Signal   Response Time
--------------------------------------------------
[BUY] Qwen3-32B           BUY      950ms
[BUY] Llama-4-Maverick-17B BUY     1200ms
[HOLD] GPT-OSS-120B       HOLD     1450ms
[BUY] Kimi-K2             BUY      1100ms

==================================================
[CONSENSUS] BUY
  Agreement: 75.0%
  Confidence: 76.5/100
  Status: TRADEABLE
==================================================

[OK] Results logged to model_comparison_v2.csv

[WAIT] Next cycle in 5 minutes...
```

---

## 📈 Análisis de Resultados

Después de ejecutar 24-48 horas, usa el notebook mejorado:

```python
# En Jupyter o VS Code
df = pd.read_csv('model_comparison_v2.csv')

# Ver estadísticas
print(df.groupby('Model_Name')['Model_Signal'].value_counts())
print(df['Confidence_Score'].describe())
print(df[df['Confidence_Score'] >= 75].shape[0])  # Operaciones válidas
```

---

## 🎓 Estrategia de Trading

### **Reglas de Entrada:**
1. ✅ Confidence Score ≥ 75%
2. ✅ Setup Score ≥ 7/10
3. ✅ Consenso de al menos 75% de modelos
4. ✅ Volatilidad < VERY HIGH

### **Reglas de Salida:**
1. 🛑 Stop Loss: -2%
2. 🎯 Take Profit: +4%
3. 📉 Trailing Stop: -1.5% desde máximo

### **Gestión de Posición:**
- Volatilidad BAJA: 100% posición
- Volatilidad MODERADA: 75% posición
- Volatilidad ALTA: 50% posición
- Volatilidad MUY ALTA: 25% posición

---

## 💡 Ventajas de V2

1. **Mayor Prudencia**: No opera sin alta confianza
2. **Mejor Contexto**: LLMs reciben 2x más información
3. **Protección Capital**: Stop-loss automático
4. **R/R Favorable**: 1:2 (ganas el doble de lo que arriesgas)
5. **Múltiples Timeframes**: Análisis corto/medio/largo plazo
6. **Volumen Confirmado**: No opera sin respaldo de volumen
7. **Diversidad**: 4 arquitecturas diferentes de LLM

---

## ⚠️ Recomendaciones

1. **Ejecutar Mínimo 1 Semana**: Para capturar diferentes condiciones
2. **Monitorear Confidence**: Si promedio < 75%, ajustar threshold
3. **Revisar Setup Scores**: Identificar patrones ganadores
4. **Comparar con V1**: Ver si mejora el rendimiento
5. **Backtesting**: Simular con datos históricos

---

## 📊 Archivos Generados

- `model_comparison_v2.csv` - Datos de todos los ciclos
- Columnas: 20 (vs 12 en V1)
- Información más detallada por operación

---

## 🔧 Personalización

### Cambiar Risk/Reward:
```python
STOP_LOSS_PERCENT = 0.01       # 1% más conservador
TAKE_PROFIT_PERCENT = 0.03     # 3% más conservador (R/R 1:3)
```

### Cambiar Confidence:
```python
CONFIDENCE_THRESHOLD = 80      # Más estricto
CONFIDENCE_THRESHOLD = 70      # Menos estricto
```

### Añadir más modelos:
```python
MODELS_V2.append({
    'name': 'nuevo-modelo',
    'display_name': 'Nuevo-Modelo',
    'description': 'Descripción',
    'temperature': 0.3,
    'rpm': 30
})
```

---

## 🎯 Objetivo

Maximizar ganancias mediante:
1. **Señales de alta calidad** (Setup Score)
2. **Consenso fuerte** (Agreement ≥75%)
3. **Protección de capital** (Stop-loss)
4. **R/R favorable** (1:2)
5. **Contexto completo** para LLMs

---

**¡Ejecuta durante 1-2 semanas y compara con V1!**

📊 Luego analiza con el notebook mejorado para determinar la mejor estrategia.
