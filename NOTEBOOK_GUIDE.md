# 📊 Model Analysis Notebook - Guía de Uso

## 🎯 Descripción

Jupyter Notebook interactivo para **análisis completo de resultados** de la comparación de modelos LLM en trading. Incluye 11 secciones con visualizaciones avanzadas.

---

## 📋 Contenido del Notebook

### **1️⃣ Importar Librerías**
- pandas, numpy, matplotlib, seaborn, plotly
- Configuración de estilos y opciones

### **2️⃣ Cargar Datos**
- Carga de `model_comparison.csv`
- Validación y vista previa de datos

### **3️⃣ Exploración y Estadísticas**
- Información del dataset
- Estadísticas descriptivas
- Detección de valores nulos

### **4️⃣ Distribución de Señales por Modelo**
- 📊 **Gráficos de pastel** para cada modelo
- Tabla resumen con porcentajes
- Cálculo de agresividad (BUY+SELL)

### **5️⃣ Comparación de Tiempos de Respuesta**
- ⚡ **Box plots** de distribución
- Barras con promedio y desviación estándar
- Ranking de velocidad

### **6️⃣ Análisis de Consenso**
- 🎯 Distribución de señales consensuadas
- Nivel de acuerdo entre modelos
- Acuerdo individual con consenso

### **7️⃣ Evolución Temporal de Señales**
- 📈 **Series temporales** por modelo
- Visualización de zonas BUY/SELL/HOLD
- Estadísticas por período

### **8️⃣ Evolución del Precio y Señales**
- 💰 **Precio de BTC** con marcadores de señales
- Nivel de acuerdo vs tiempo
- Análisis de precisión de señales

### **9️⃣ Visualización Interactiva (Plotly)**
- 🔍 **Gráficos interactivos** con hover
- Scatter plots por modelo
- Box plots interactivos

### **🔟 Heatmap de Correlaciones**
- 🔥 **Matriz de correlación** entre variables
- Interpretación automática
- Top 5 correlaciones

### **1️⃣1️⃣ Ranking Final de Modelos**
- 🏆 **Radar chart** multidimensional
- Puntuación ponderada
- Recomendaciones por objetivo

---

## 🚀 Cómo Usar

### **Prerequisitos**

```bash
pip install jupyter pandas numpy matplotlib seaborn plotly
```

### **Opción 1: Jupyter Notebook**

```bash
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Iniciar Jupyter
jupyter notebook

# Abrir: model_analysis.ipynb
```

### **Opción 2: VS Code**

1. Abrir `model_analysis.ipynb` en VS Code
2. Seleccionar kernel Python (.venv)
3. Ejecutar celdas con `Shift+Enter`

### **Opción 3: JupyterLab**

```bash
jupyter lab
```

---

## 📊 Requisitos de Datos

El notebook requiere el archivo **`model_comparison.csv`** en la misma carpeta.

### **Generar datos:**

```bash
# Ejecutar bot de comparación
python model_comparison.py

# Dejar corriendo al menos 2-4 horas
# Luego abrir el notebook
```

### **Estructura esperada del CSV:**

```csv
Timestamp,Cycle,Symbol,Price,RSI,MACD_Signal,Trend,Model_Name,Model_Signal,Model_Response_Time_ms,Consensus_Signal,Agreement_Level
2025-10-16 10:00:00,1,BTCUSDT,67500.00,58.45,BULLISH,BULLISH/BULLISH,Llama-3.3-70B,BUY,1250,BUY,75.0
...
```

---

## 🎨 Tipos de Visualizaciones

### **Gráficos Estáticos (matplotlib/seaborn)**
- ✅ Pie charts (distribución de señales)
- ✅ Box plots (tiempos de respuesta)
- ✅ Bar charts (comparaciones)
- ✅ Line plots (series temporales)
- ✅ Scatter plots (precio vs señales)
- ✅ Heatmaps (correlaciones)
- ✅ Radar charts (ranking multidimensional)

### **Gráficos Interactivos (plotly)**
- ✅ Scatter con hover (señales interactivas)
- ✅ Box plots interactivos
- ✅ Zoom y pan
- ✅ Exportar como imagen

---

## 📈 Métricas Analizadas

### **Por Modelo:**
- Distribución de señales (BUY/SELL/HOLD %)
- Tiempo de respuesta (promedio, mediana, std)
- Acuerdo con consenso (%)
- Agresividad (% de operaciones activas)

### **De Consenso:**
- Distribución de señales consensuadas
- Nivel de acuerdo promedio
- Casos de unanimidad (100%)
- Casos de desacuerdo (<50%)

### **Temporales:**
- Evolución de precio
- Evolución de señales
- Precisión de predicciones

### **Ranking:**
- Puntuación de velocidad
- Puntuación de consenso
- Puntuación de agresividad
- **Puntuación total ponderada**

---

## 🏆 Interpretación de Resultados

### **Mejor Modelo General**
→ Mayor puntuación total (combinación equilibrada)

### **Mejor para Trading Rápido**
→ Menor tiempo de respuesta (Llama-3.1-8B)

### **Mejor para Consenso**
→ Mayor acuerdo con otros modelos (Llama-3.3-70B)

### **Más Agresivo**
→ Mayor % de BUY+SELL (más operaciones)

### **Más Conservador**
→ Mayor % de HOLD (menos operaciones)

---

## 💡 Tips de Uso

### **Filtrar por período de tiempo:**

```python
# Últimas 24 horas
recent_df = df[df['Timestamp'] >= df['Timestamp'].max() - pd.Timedelta(hours=24)]
```

### **Analizar modelo específico:**

```python
# Solo Llama-3.3-70B
llama_70b = df[df['Model_Name'] == 'Llama-3.3-70B']
```

### **Exportar resultados:**

```python
# Guardar ranking
ranking_df.to_csv('model_ranking.csv', index=False)
```

### **Actualizar datos:**

```python
# Recargar después de más ejecuciones
df = pd.read_csv('model_comparison.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
```

---

## 🔧 Personalización

### **Cambiar colores:**

```python
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']  # Tus colores
```

### **Ajustar pesos del ranking:**

```python
ranking_df['Puntuación Total'] = (
    ranking_df['Score_Velocidad'] * 0.5 +      # Más peso a velocidad
    ranking_df['Score_Consenso'] * 0.3 +
    ranking_df['Score_Agresividad'] * 0.2
)
```

### **Agregar nuevas visualizaciones:**

Copia y modifica celdas existentes, o agrega nuevas al final del notebook.

---

## 🐛 Solución de Problemas

### **Error: "FileNotFoundError: model_comparison.csv"**

```bash
# Ejecutar primero:
python model_comparison.py
```

### **Error: "ModuleNotFoundError: No module named 'plotly'"**

```bash
pip install plotly
```

### **Gráficos no se muestran**

```python
# Agregar al inicio del notebook:
%matplotlib inline
```

### **Kernel muerto/reiniciado**

```python
# Reiniciar kernel: Kernel → Restart
# Ejecutar todas las celdas: Cell → Run All
```

---

## 📊 Ejemplo de Output

### **Tabla de Ranking:**

| Modelo | Velocidad (ms) | Acuerdo Consenso (%) | Agresividad (%) | Puntuación Total |
|--------|----------------|----------------------|-----------------|------------------|
| 🥇 Llama-3.1-8B | 485 | 82.5 | 66.7 | 85.4 |
| 🥈 Llama-4-Scout-17B | 820 | 85.0 | 62.5 | 83.1 |
| 🥉 Llama-3.3-70B | 1245 | 87.5 | 58.3 | 78.9 |
| ⚪ Qwen3-32B | 1005 | 78.3 | 52.5 | 72.6 |

---

## 📚 Recursos Adicionales

- **MODEL_COMPARISON_GUIDE.md** - Guía del sistema de comparación
- **EXAMPLE_OUTPUT.md** - Ejemplos de salidas
- **analyze_models.py** - Script de análisis por terminal

---

## 🤝 Contribuir

Si agregas nuevas visualizaciones o mejoras:

```bash
git add model_analysis.ipynb
git commit -m "Add: nueva visualización de X"
git push
```

---

## 📞 Soporte

**GitHub:** https://github.com/amaliogomezlopez/TRADING_LLMS  
**Issues:** https://github.com/amaliogomezlopez/TRADING_LLMS/issues

---

🚀 **¡Disfruta analizando tus modelos LLM!**
