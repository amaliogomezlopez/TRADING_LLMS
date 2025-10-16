# 🤖 Trading Bot with LLM & Technical Analysis

Un bot de trading automatizado que utiliza **Large Language Models (LLM)** combinado con **análisis técnico avanzado** para tomar decisiones de compra/venta en el mercado de criptomonedas. El bot opera en la **testnet de Binance** para pruebas sin riesgo real.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [🆕 Comparación de Modelos LLM](#-comparación-de-modelos-llm)
- [📊 Notebook de Análisis Visual](#-notebook-de-análisis-visual)
- [Análisis de Resultados](#-análisis-de-resultados)
- [Gestión de Riesgo](#️-gestión-de-riesgo)
- [Roadmap](#-roadmap)
- [Contribuciones](#-contribuciones)
- [Disclaimer](#-disclaimer)

---

## ✨ Características

### 🧠 Inteligencia Artificial
- **LLM (Groq/Llama 3.1)**: Analiza datos técnicos y toma decisiones de trading
- **Prompt Engineering**: Contexto técnico enriquecido para decisiones informadas
- **Validación de señales**: Múltiples confirmaciones antes de ejecutar operaciones

### 📊 Análisis Técnico Completo
- **RSI (Relative Strength Index)**: Detecta condiciones de sobrecompra/sobreventa
- **MACD**: Identifica cambios de momentum y tendencias
- **EMAs (9 y 21)**: Análisis de tendencias de corto y medio plazo
- **Bollinger Bands**: Medición de volatilidad y niveles extremos

### 🛡️ Gestión de Riesgo Avanzada
- **Stop Loss Automático**: Protección del 2% en cada posición
- **Take Profit Automático**: Objetivo del 3% por operación
- **Límite de Pérdidas Totales**: El bot se detiene si las pérdidas superan el umbral
- **Risk/Reward**: Ratio de 1.5:1 (3% ganancia / 2% pérdida)

### 📈 Monitoreo y Análisis
- **Logging Detallado**: Registro CSV con todas las operaciones e indicadores
- **Script de Análisis**: Estadísticas de performance, win rate, P&L
- **Tracking en Tiempo Real**: Visualización de P&L realizado y no realizado

---

## 🏗️ Arquitectura

```
┌─────────────────┐
│  Binance API    │ ← Datos de mercado (OHLCV)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  Technical Analysis Engine  │
│  • RSI, MACD, EMAs, BB     │
│  • Trend Detection          │
│  • Signal Validation        │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│      LLM (Groq API)         │
│  • Contextual Analysis      │
│  • Decision Making          │
│  • BUY / SELL / HOLD        │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   Risk Management Module    │
│  • Stop Loss / Take Profit  │
│  • Position Sizing          │
│  • Max Loss Limit           │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│    Order Execution          │
│  (Binance Testnet)          │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│    Logging & Analysis       │
│  • CSV Logs                 │
│  • Performance Metrics      │
└─────────────────────────────┘
```

---

## 🛠️ Tecnologías

### Core
- **Python 3.8+**: Lenguaje principal
- **python-binance**: Integración con Binance API
- **groq**: Cliente para LLM (Llama 3.1)
- **python-dotenv**: Gestión de variables de entorno

### Análisis Técnico
- **ta (Technical Analysis Library)**: Cálculo de indicadores
- **pandas**: Manipulación de datos de series temporales
- **numpy**: Operaciones numéricas

### APIs
- **Binance Testnet**: Simulación de trading sin riesgo
- **Groq API**: Acceso a modelos LLM de alta velocidad

---

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/amaliogomezlopez/TRADING_LLMS.git
cd TRADING_LLMS
```

### 2. Crear entorno virtual

**Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install python-binance groq python-dotenv ta pandas numpy
```

---

## ⚙️ Configuración

### 1. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Binance Testnet API Keys
BINANCE_API_KEY=tu_testnet_api_key_aqui
BINANCE_API_SECRET=tu_testnet_secret_key_aqui

# Groq API Key
GROQ_API_KEY=tu_groq_api_key_aqui
```

> **📝 Nota**: 
> - Obtén tus credenciales de Binance Testnet en: [testnet.binance.vision](https://testnet.binance.vision/)
> - Obtén tu API key de Groq en: [console.groq.com](https://console.groq.com/)

### 2. Parámetros de Trading

Edita `trading_bot.py` para ajustar los parámetros según tu estrategia:

```python
# Trading Parameters
SYMBOL = 'BTCUSDT'              # Par de trading
QUANTITY = 0.001                 # Cantidad por operación
INTERVAL = Client.KLINE_INTERVAL_15MINUTE  # Timeframe

# Risk Management
STOP_LOSS_PERCENT = 0.02        # 2% stop loss
TAKE_PROFIT_PERCENT = 0.03      # 3% take profit
MAX_TOTAL_LOSS = -100.0         # Pérdida máxima en USDT

# Technical Indicators
RSI_PERIOD = 14
RSI_OVERSOLD = 30               # Umbral de sobreventa
RSI_OVERBOUGHT = 70             # Umbral de sobrecompra
EMA_SHORT = 9
EMA_LONG = 21
```

---

## 🚀 Uso

### Ejecutar el Bot

```bash
python trading_bot.py
```

El bot mostrará información en tiempo real:

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

## 🆕 Comparación de Modelos LLM

### 🤖 Sistema Multi-Modelo

¿Quieres saber qué modelo LLM es mejor para trading? El sistema de comparación ejecuta **4 modelos simultáneamente** y calcula un consenso entre sus decisiones.

### Modelos Incluidos

1. **Llama-3.3-70B** (70B params) - El más inteligente
2. **Llama-3.1-8B** (8B params) - El más rápido ⚡
3. **Llama-4-Scout-17B** (17B params) - Última generación
4. **Qwen3-32B** (32B params) - Arquitectura alternativa

### Ejecutar Comparación

```powershell
# Iniciar comparación (ejecutar durante 24-48 horas)
python model_comparison.py

# Analizar resultados
python analyze_models.py
```

### Métricas Analizadas

- ✅ **Tiempo de respuesta** - Velocidad de decisión
- ✅ **Distribución de señales** - BUY/SELL/HOLD %
- ✅ **Acuerdo con consenso** - Qué modelo es más "mainstream"
- ✅ **Agresividad** - Ratio de operaciones vs espera
- ✅ **Unanimidad** - Ciclos donde todos coinciden
- ✅ **Desacuerdos** - Casos de máxima divergencia

### Datos Guardados

Archivo: `model_comparison.csv`
- Timestamp, precio, indicadores técnicos
- Señal de cada modelo individual
- Tiempo de respuesta de cada modelo
- Consenso calculado
- Nivel de acuerdo (%)

**📖 Ver guía completa:** [MODEL_COMPARISON_GUIDE.md](MODEL_COMPARISON_GUIDE.md)

---

## 📊 Notebook de Análisis Visual

### 🎨 Análisis Interactivo con Jupyter

Hemos creado un **notebook completo con 11 secciones de visualizaciones** para analizar los resultados:

```bash
# Instalar Jupyter (si no lo tienes)
pip install jupyter plotly

# Abrir notebook
jupyter notebook model_analysis.ipynb

# O en VS Code: abrir model_analysis.ipynb
```

### Visualizaciones Incluidas:

1. **📊 Distribución de señales** - Gráficos de pastel por modelo
2. **⚡ Tiempos de respuesta** - Box plots y estadísticas
3. **🎯 Análisis de consenso** - Nivel de acuerdo entre modelos
4. **📈 Evolución temporal** - Series de tiempo de señales
5. **💰 Precio vs señales** - Efectividad de predicciones
6. **🔍 Gráficos interactivos** - Plotly con hover y zoom
7. **🔥 Heatmap de correlaciones** - Relaciones entre variables
8. **🏆 Ranking final** - Radar charts y puntuaciones

### Características del Notebook:

- ✅ **11 secciones** con análisis completo
- ✅ **Gráficos estáticos** (matplotlib/seaborn)
- ✅ **Gráficos interactivos** (plotly)
- ✅ **Estadísticas detalladas** por modelo
- ✅ **Ranking multidimensional** con puntuación ponderada
- ✅ **Recomendaciones automáticas** por objetivo

**📖 Ver guía completa:** [NOTEBOOK_GUIDE.md](NOTEBOOK_GUIDE.md)

---

## 📊 Análisis de Resultados

### Script de Análisis

Ejecuta el script de análisis para ver estadísticas detalladas:

```bash
python analyze_performance.py
```

**Output:**

```
============================================================
📊 ANÁLISIS DEL TRADING BOT
============================================================

📅 PERÍODO:
   Primer registro: 2025-10-13 08:00:00
   Último registro: 2025-10-13 18:00:00
   Total de ciclos: 40

🤖 SEÑALES DEL LLM:
   BUY: 12 (30.0%)
   SELL: 8 (20.0%)
   HOLD: 20 (50.0%)

💰 TRADES:
   Compras (BUY): 12
   Ventas (SELL): 12

📈 PERFORMANCE:
   Trades completados: 12
   Trades ganadores: 8
   Trades perdedores: 4
   Win Rate: 66.7%

💵 P&L:
   Total P&L: $45.50
   Average P&L por trade: $3.79
   Average ganancia: $8.25
   Average pérdida: -$4.12

📊 MÉTRICAS DE RIESGO:
   Profit Factor: 1.60
```

### Archivo de Log

Todos los trades se registran en `trading_log.csv`:

| Timestamp | Symbol | LLM_Signal | Action_Taken | Price | RSI | MACD | Trade_PNL | Total_PNL |
|-----------|--------|------------|--------------|-------|-----|------|-----------|-----------|
| 2025-10-13 14:30 | BTCUSDT | BUY | BUY | 62450 | 45 | BULLISH | - | 0.00 |
| 2025-10-13 15:00 | BTCUSDT | SELL | SELL | 64100 | 72 | BEARISH | 1.65 | 1.65 |

---

## 🛡️ Gestión de Riesgo

### Stop Loss Automático
- Se activa cuando el precio cae **2%** desde la entrada
- Cierra automáticamente la posición
- Protege contra pérdidas mayores

### Take Profit Automático
- Se activa cuando el precio sube **3%** desde la entrada
- Asegura ganancias automáticamente
- Evita dar back profits por codicia

### Límite de Pérdidas Máximo
- El bot se **detiene automáticamente** si las pérdidas totales superan $100
- Previene desastres financieros
- Permite revisar la estrategia antes de continuar

### Validación de Señales
- Las compras solo se ejecutan si:
  - El LLM sugiere BUY **Y**
  - La tendencia es favorable **O** el RSI está en sobreventa
- Reduce señales falsas y mejora la calidad de las entradas

---

## 🗺️ Roadmap

### ✅ Completado
- [x] Integración con Binance Testnet
- [x] LLM para toma de decisiones
- [x] Análisis técnico completo (RSI, MACD, EMAs, BB)
- [x] Gestión de riesgo automática
- [x] Logging detallado
- [x] Script de análisis de performance

### 🔜 Próximamente
- [ ] Backtesting con datos históricos
- [ ] Optimización de parámetros con Grid Search
- [ ] Multi-symbol trading (múltiples pares simultáneos)
- [ ] Dashboard web con visualizaciones en tiempo real
- [ ] Alertas por Telegram/Email
- [ ] Análisis de volumen
- [ ] Sentiment analysis de noticias
- [ ] Machine Learning para predicción de precios
- [ ] Multi-timeframe analysis

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Si quieres mejorar el proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## ⚠️ Disclaimer

**IMPORTANTE: Este bot es solo para fines educativos y de investigación.**

- ⚠️ **NO** usar con dinero real sin pruebas exhaustivas
- ⚠️ El trading de criptomonedas conlleva **alto riesgo**
- ⚠️ Las pérdidas pueden ser **totales**
- ⚠️ Este software se proporciona "AS IS" sin garantías de ningún tipo
- ⚠️ El autor **NO** se hace responsable de pérdidas financieras

**Recomendaciones:**
1. Prueba extensivamente en **testnet** antes de considerar uso real
2. Nunca inviertas más de lo que puedas permitirte perder
3. Realiza tu propia investigación y análisis
4. Consulta con un asesor financiero profesional

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Amalio Gómez López**

- GitHub: [@amaliogomezlopez](https://github.com/amaliogomezlopez)
- Proyecto: [TRADING_LLMS](https://github.com/amaliogomezlopez/TRADING_LLMS)

---

## 🙏 Agradecimientos

- [Binance](https://www.binance.com/) - API de trading
- [Groq](https://groq.com/) - Infraestructura LLM de alta velocidad
- [Technical Analysis Library](https://github.com/bukosabino/ta) - Indicadores técnicos
- Comunidad de Python y trading algorítmico

---

## 📚 Recursos Adicionales

### Documentación
- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [Technical Analysis Library](https://technical-analysis-library-in-python.readthedocs.io/)
- [Groq API Docs](https://console.groq.com/docs)

### Tutoriales
- [Aprende Trading Algorítmico](https://www.investopedia.com/articles/active-trading/101014/basics-algorithmic-trading-concepts-and-examples.asp)
- [Análisis Técnico para Principiantes](https://www.babypips.com/learn/forex)

---

<div align="center">

### ⭐ Si este proyecto te resulta útil, considera darle una estrella!

**Made with ❤️ and Python**

</div>
