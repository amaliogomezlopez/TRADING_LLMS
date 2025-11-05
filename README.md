# 🤖 Trading con LLMs: Experimento de Trading Automatizado con Inteligencia Artificial

[![YouTube Channel](https://img.shields.io/badge/YouTube-AmalioMetria-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/@AmalioMetria) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

## 📖 Descripción

Experimento real de trading automatizado donde **8 modelos de lenguaje (LLMs)** compiten para generar beneficios operando con Bitcoin. Durante 20 días, diferentes IAs analizaron 12 indicadores técnicos y tomaron decisiones de compra/venta cada 5 minutos.

**Resultado sorprendente:** Un modelo ganó **+6.92%** con una sola operación, mientras otros hicieron cientos de trades y perdieron dinero.

🎥 **[Ver video completo del experimento en YouTube](https://youtu.be/408Rty_qlrg)**

---

## 🎯 Objetivos

- Evaluar la capacidad de diferentes LLMs para tomar decisiones de trading
- Comparar estrategias conservadoras vs activas
- Medir el valor añadido real (Alpha) de cada modelo
- Demostrar que cantidad de operaciones ≠ beneficios

---

## 🧪 Experimentos Realizados

### 📊 Experimento V1 (13 días: 13-26 Oct 2025)
- **Duración:** 13 días continuos
- **Datos:** 14,128 registros
- **Análisis:** [Ver análisis completo V1](docs/ANALISIS_RESULTADOS_V1.md)

### 📊 Experimento V2 (7 días: 27 Oct - 2 Nov 2025)
- **Duración:** 7 días continuos
- **Datos:** 6,000+ registros
- **Análisis:** [Ver análisis completo V2](docs/ANALISIS_RESULTADOS_V2.md)

### 🔍 Comparación V1 vs V2
- [Ver comparación detallada](docs/COMPARACION_V1_V2.md)

---

## 🏆 Resultados

### Ranking por Alpha (Valor Añadido Real)

| Pos | Modelo | Exp | ROI | Alpha | Trades |
|-----|--------|-----|-----|-------|--------|
| 🥇 | **Qwen3-32B** | V1 | **+6.92%** | **+7.17pp** | 1 |
| 🥈 | **Kimi-K2** | V2 | **+7.73%** | **+2.93pp** | 11 |
| 🥉 | **Llama-3.3-70B** | V1 | **+1.66%** | **+1.91pp** | 313 |
| 4º | Llama-3.1-8B | V1 | -2.07% | -1.82pp | 273 |
| 5º | Llama-4-Scout-17B | V1 | -2.71% | -2.46pp | 179 |
| 6º | Qwen3-32B | V2 | +4.74% | -0.05pp | 6 |
| 7º | Llama-4-Maverick | V2 | 0.00% | -4.79pp | 0 |
| 8º | GPT-OSS-120B | V2 | 0.00% | -4.79pp | 0 |

**Alpha = ROI del Modelo - ROI del Mercado**

---

## 💡 Lecciones Aprendidas

- 1 operación perfecta > 273 mediocres
- El mercado fue lateral (-0.25%) durante el experimento
- Las métricas clave están en los documentos dentro de `docs/`

---

## 🔧 Instalación rápida (Windows PowerShell)

```powershell
# Clonar repositorio
git clone https://github.com/amaliogomezlopez/TRADING_LLMS.git
cd TRADING_LLMS

# Crear entorno virtual e instalar dependencias
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🚀 Uso rápido

```powershell
# Análisis V1
python scripts/analyze_v1_results.py

# Análisis V2
python scripts/analyze_v2_results.py
```

---

## 📞 Contacto

- 🎥 YouTube: [@AmalioMetria](https://www.youtube.com/@AmalioMetria)
- 👨‍💻 Autor: Amalio Gómez López
- 📁 GitHub: [amaliogomezlopez/TRADING_LLMS](https://github.com/amaliogomezlopez/TRADING_LLMS)

---


