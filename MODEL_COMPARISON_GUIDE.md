# 🤖 GUÍA DE COMPARACIÓN DE MODELOS LLM

## 📋 Descripción

Sistema para **comparar el rendimiento de 4 modelos LLM diferentes** en trading de criptomonedas. Todos los modelos analizan los mismos datos técnicos simultáneamente y se calcula un **consenso** entre sus decisiones.

---

## 🧠 Modelos Seleccionados

### 1️⃣ **Llama-3.3-70B** (`llama-3.3-70b-versatile`)
- **Parámetros:** 70 mil millones
- **Ventaja:** El más inteligente, mejor razonamiento complejo
- **Velocidad:** Media (12K TPM)
- **Ideal para:** Análisis profundo de patrones complejos

### 2️⃣ **Llama-3.1-8B** (`llama-3.1-8b-instant`) ✅ ACTUAL
- **Parámetros:** 8 mil millones  
- **Ventaja:** El más rápido, mejor balance velocidad/calidad
- **Velocidad:** Rápida (6K TPM, 500K TPD)
- **Ideal para:** Trading de alta frecuencia

### 3️⃣ **Llama-4-Scout-17B** (`meta-llama/llama-4-scout-17b-16e-instruct`)
- **Parámetros:** 17 mil millones
- **Ventaja:** Última generación Llama 4, más tokens disponibles
- **Velocidad:** Rápida (30K TPM)
- **Ideal para:** Balance entre inteligencia y velocidad

### 4️⃣ **Qwen3-32B** (`qwen/qwen3-32b`)
- **Parámetros:** 32 mil millones
- **Ventaja:** Arquitectura diferente (modelo chino), perspectiva alternativa
- **Velocidad:** Media (6K TPM, 500K TPD)
- **Ideal para:** Diversificación de enfoques

---

## 🚀 Uso

### **Paso 1: Ejecutar Comparación**

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Ejecutar comparación de modelos
python model_comparison.py
```

El script:
- ✅ Consulta los **4 modelos simultáneamente** cada ciclo
- ✅ Calcula un **consenso** entre las decisiones
- ✅ Guarda resultados en `model_comparison.csv`
- ✅ Muestra tiempo de respuesta de cada modelo
- ✅ Indica nivel de acuerdo entre modelos

### **Paso 2: Analizar Resultados**

```powershell
# Ejecutar análisis
python analyze_models.py
```

**Opciones del menú:**

1. **Analizar todos los datos** - Desde el inicio
2. **Últimas 2 horas** - Ciclos recientes
3. **Últimas 6 horas** - Sesión de trading
4. **Últimas 24 horas** - Día completo
5. **Patrones de señales** - Unanimidad y desacuerdos
6. **Exportar resumen** - Crear `model_summary.csv`

---

## 📊 Datos Guardados

### **Archivo: `model_comparison.csv`**

Columnas:
- `Timestamp` - Fecha/hora del análisis
- `Cycle` - Número de ciclo
- `Symbol` - Par trading (BTCUSDT)
- `Price` - Precio actual
- `RSI` - Indicador RSI
- `MACD_Signal` - Señal MACD
- `Trend` - Tendencia corto/mediano plazo
- `Model_Name` - Nombre del modelo
- `Model_Signal` - Decisión del modelo (BUY/SELL/HOLD)
- `Model_Response_Time_ms` - Tiempo de respuesta en milisegundos
- `Consensus_Signal` - Decisión consensuada
- `Agreement_Level` - % de acuerdo entre modelos

**Importante:** Cada ciclo genera **4 filas** (una por modelo)

---

## 📈 Métricas de Comparación

### **1. Distribución de Señales**
- **BUY %** - Porcentaje de señales de compra
- **SELL %** - Porcentaje de señales de venta
- **HOLD %** - Porcentaje de señales de espera
- **Agresividad** = (BUY + SELL) / Total

### **2. Tiempo de Respuesta**
- Promedio en milisegundos
- Modelos más rápidos = mejor para trading de alta frecuencia

### **3. Acuerdo con Consenso**
- % de veces que coincide con la decisión mayoritaria
- Mayor acuerdo = modelo más "mainstream"
- Menor acuerdo = modelo con perspectiva diferente

### **4. Consenso General**
- **Nivel de acuerdo** - % de modelos que coinciden
- **100%** = Unanimidad (todos de acuerdo)
- **75%** = 3 de 4 modelos coinciden
- **50%** = Empate (máximo desacuerdo)

---

## 🏆 Cómo Interpretar los Resultados

### **Modelo "Mejor"**

No hay un "mejor absoluto", depende del objetivo:

#### **Si buscas VELOCIDAD:**
- Prioriza: **Menor tiempo de respuesta**
- Mejor modelo: Probablemente Llama-3.1-8B

#### **Si buscas PRECISIÓN:**
- Prioriza: **Mayor acuerdo con consenso**
- Mejor modelo: El que más coincide con la decisión mayoritaria

#### **Si buscas OPORTUNIDADES:**
- Prioriza: **Mayor agresividad (BUY+SELL)**
- Mejor modelo: El que menos señales HOLD genera

#### **Si buscas DIVERSIFICACIÓN:**
- Prioriza: **Menor acuerdo con consenso**
- Mejor modelo: El que tiene perspectiva diferente (probablemente Qwen3)

---

## 💡 Estrategias de Uso

### **Estrategia 1: Consenso Mayoritario**
```python
if agreement_level >= 75:  # 3 de 4 modelos
    execute_signal(consensus_signal)
else:
    HOLD  # Esperar mayor claridad
```

### **Estrategia 2: Unanimidad**
```python
if agreement_level == 100:  # Todos de acuerdo
    execute_signal(consensus_signal)
    # Máxima confianza
```

### **Estrategia 3: Mejor Modelo Individual**
```python
# Usar solo el modelo con mayor performance histórico
best_model = analyze_historical_performance()
execute_signal(best_model.signal)
```

### **Estrategia 4: Ponderación**
```python
# Ponderar por performance pasada
signal_weights = {
    'Llama-3.3-70B': 0.4,     # Mayor peso al más inteligente
    'Llama-3.1-8B': 0.3,
    'Llama-4-Scout-17B': 0.2,
    'Qwen3-32B': 0.1
}
```

---

## ⚡ Optimización

### **Reducir Tiempo de Espera**

Actualmente: **5 minutos por ciclo**

Para comparaciones más rápidas (solo pruebas):

```yaml
# config.yml
trading:
  timeframe: "1m"  # 1 minuto
```

**⚠️ ADVERTENCIA:** Timeframes muy cortos generan más comisiones y ruido.

### **Ejecutar en Paralelo**

Para trading real, puedes ejecutar ambos:

```powershell
# Terminal 1: Bot original
python trading_bot.py

# Terminal 2: Comparación de modelos
python model_comparison.py
```

---

## 📋 Checklist de Análisis

Después de **24 horas** de datos:

- [ ] Ejecutar `analyze_models.py` opción 4 (últimas 24h)
- [ ] Verificar tiempo de respuesta promedio
- [ ] Identificar modelo con mayor acuerdo
- [ ] Revisar distribución de señales (BUY/SELL/HOLD)
- [ ] Analizar casos de unanimidad vs desacuerdo
- [ ] Exportar resumen a CSV (opción 6)
- [ ] Decidir estrategia de consenso

Después de **1 semana**:

- [ ] Comparar performance vs `trading_log.csv` (bot original)
- [ ] Evaluar si el consenso mejora resultados
- [ ] Identificar modelo más rentable
- [ ] Ajustar pesos de ponderación
- [ ] Documentar patrones encontrados

---

## 🎯 Preguntas Frecuentes

### **¿Es más lento que el bot original?**

**Sí**, 4x más lento porque consulta 4 modelos en serie. Cada ciclo tarda ~2-4 segundos más.

**Solución:** El análisis vale la pena para identificar el mejor modelo, luego puedes usar solo ese en `trading_bot.py`.

### **¿Consumo de API?**

**4x más llamadas** a Groq API (pero estás en free tier con límites generosos).

Límite Groq free: 30 RPM, 14.4K RPD
- Bot original: 1 llamada/5min = 288 llamadas/día ✅
- Comparación: 4 llamadas/5min = 1152 llamadas/día ✅ (aún dentro del límite)

### **¿Puedo agregar más modelos?**

**Sí**, solo edita la lista `MODELS_TO_TEST` en `model_comparison.py`:

```python
MODELS_TO_TEST = [
    # ... modelos existentes ...
    {
        'name': 'gemma-7b-it',
        'display_name': 'Gemma-7B',
        'description': 'Google Gemma model',
        'temperature': 0.3
    }
]
```

### **¿Cuál es el "mejor" modelo?**

**Depende de tus métricas:**
- **Velocidad** → Llama-3.1-8B
- **Inteligencia** → Llama-3.3-70B  
- **Novedad** → Llama-4-Scout-17B
- **Diversidad** → Qwen3-32B

Después de 24-48 horas de datos, tendrás evidencia empírica.

---

## 🔄 Workflow Completo

```
1. Ejecutar model_comparison.py (dejar corriendo 24-48h)
   ↓
2. Analizar resultados con analyze_models.py
   ↓
3. Identificar modelo con mejor performance
   ↓
4. Modificar trading_bot.py para usar ese modelo
   ↓
5. Ejecutar trading_bot.py con configuración optimizada
   ↓
6. Comparar resultados vs período de prueba
   ↓
7. Iterar: volver a comparar si mercado cambia
```

---

## 📊 Ejemplo de Salida

```
================================================================================
CYCLE #15 - 2025-10-13 14:30:00
================================================================================

📊 MARKET DATA:
   Price: $114,247.14 (+1.23%)
   RSI: 58.45 - NEUTRAL
   MACD: BULLISH
   Trend: BULLISH / BULLISH

🤖 MODEL PREDICTIONS:
Model                     Signal   Response Time
--------------------------------------------------
✅ Llama-3.3-70B          BUY      1250ms
✅ Llama-3.1-8B           BUY      450ms
✅ Llama-4-Scout-17B      BUY      780ms
⏸️ Qwen3-32B              HOLD     920ms

==================================================
📊 CONSENSUS: BUY (75.0% agreement)
==================================================
```

---

## 🎓 Conclusión

Este sistema te permite:

✅ **Comparar 4 modelos LLM** objetivamente  
✅ **Identificar el mejor** para tu estrategia  
✅ **Usar consenso** para decisiones más seguras  
✅ **Optimizar performance** basado en datos reales  

**Recomendación:** Ejecuta durante 24-48 horas, analiza resultados, y luego decide qué estrategia usar en producción.

---

🚀 **¡Feliz trading con IA!**
