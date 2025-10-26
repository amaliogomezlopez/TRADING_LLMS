"""
Análisis detallado de resultados de model_comparison_v2.csv
"""

import pandas as pd
import numpy as np

# Cargar datos
df = pd.read_csv('model_comparison_v2.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

print("="*80)
print("[ANÁLISIS] RESULTADOS DE MODEL_COMPARISON_V2.CSV")
print("="*80)

# Estadísticas generales
print(f"\n[INFO] Estadísticas Generales:")
print(f"  Total de registros: {len(df)}")
print(f"  Período: {df['Timestamp'].min()} a {df['Timestamp'].max()}")
print(f"  Duración: {(df['Timestamp'].max() - df['Timestamp'].min()).days} días, {(df['Timestamp'].max() - df['Timestamp'].min()).seconds // 3600} horas")
print(f"  Ciclos únicos: {df['Cycle'].nunique()}")
print(f"  Modelos: {df['Model_Name'].nunique()}")

# Precio de Bitcoin
price_data = df.groupby('Cycle').first()
initial_price = price_data['Price'].iloc[0]
final_price = price_data['Price'].iloc[-1]
price_change = ((final_price - initial_price) / initial_price) * 100

print(f"\n[MERCADO] Bitcoin:")
print(f"  Precio Inicial: ${initial_price:,.2f}")
print(f"  Precio Final: ${final_price:,.2f}")
print(f"  Cambio: {price_change:+.2f}%")
print(f"  Máximo: ${price_data['Price'].max():,.2f}")
print(f"  Mínimo: ${price_data['Price'].min():,.2f}")

market_type = "BAJISTA" if price_change < -2 else "ALCISTA" if price_change > 2 else "LATERAL"
print(f"  Tipo de Mercado: {market_type}")

# Análisis por modelo
print(f"\n[SEÑALES] Distribución por Modelo:")
print("="*80)

models = df['Model_Name'].unique()
for model in models:
    model_df = df[df['Model_Name'] == model]
    signals = model_df['Model_Signal'].value_counts()
    total = len(model_df)
    
    print(f"\n{model}:")
    print(f"  Total señales: {total}")
    for signal, count in signals.items():
        pct = (count / total) * 100
        print(f"    {signal}: {count} ({pct:.1f}%)")

# Simulación de trading
print(f"\n[SIMULACIÓN] Beneficios/Pérdidas:")
print("="*80)

def simulate_trading(model_df, initial_cash=10000):
    model_df = model_df.sort_values('Timestamp').reset_index(drop=True)
    cash = initial_cash
    btc = 0
    trades = []
    
    for idx, row in model_df.iterrows():
        price = row['Price']
        signal = str(row['Model_Signal']).upper()
        
        if signal == 'BUY' and cash > 0:
            btc = cash / price
            cash = 0
            trades.append({'type': 'BUY', 'price': price, 'timestamp': row['Timestamp']})
        elif signal == 'SELL' and btc > 0:
            cash = btc * price
            btc = 0
            trades.append({'type': 'SELL', 'price': price, 'timestamp': row['Timestamp']})
    
    final_value = cash + (btc * model_df['Price'].iloc[-1])
    return final_value, len(trades), trades

results = {}
for model in models:
    model_df = df[df['Model_Name'] == model]
    final_value, num_trades, trades = simulate_trading(model_df)
    profit = final_value - 10000
    roi = (profit / 10000) * 100
    
    results[model] = {
        'final_value': final_value,
        'profit': profit,
        'roi': roi,
        'num_trades': num_trades,
        'trades': trades
    }
    
    emoji = "[+]" if profit > 0 else "[-]" if profit < 0 else "[=]"
    print(f"\n{emoji} {model}:")
    print(f"    Capital Final: ${final_value:,.2f}")
    print(f"    Beneficio: ${profit:+,.2f}")
    print(f"    ROI: {roi:+.2f}%")
    print(f"    Trades ejecutados: {num_trades}")

# Comparación con Hold
hold_final = (final_price / initial_price) * 10000
hold_profit = hold_final - 10000
hold_roi = (hold_profit / 10000) * 100

print(f"\n[HOLD] Estrategia Buy & Hold:")
print(f"  Capital Final: ${hold_final:,.2f}")
print(f"  Beneficio: ${hold_profit:+,.2f}")
print(f"  ROI: {hold_roi:+.2f}%")

# Comparación con Hold
print(f"\n[COMPARACIÓN] Modelos vs Hold:")
print("="*80)
for model, data in results.items():
    diff = data['roi'] - hold_roi
    status = "MEJOR" if diff > 0 else "PEOR" if diff < 0 else "IGUAL"
    emoji = "[+]" if diff > 0 else "[-]" if diff < 0 else "[=]"
    print(f"{emoji} {model}: {data['roi']:+.2f}% ({status} que Hold: {diff:+.2f}pp)")

# Análisis de por qué solo 2 modelos obtienen beneficios
print(f"\n[ANÁLISIS] ¿Por qué solo Kimi y Qwen obtienen beneficios?")
print("="*80)

# Verificar qué modelos compraron y cuándo
print(f"\nTrades ejecutados por modelo:")
for model, data in results.items():
    trades = data['trades']
    if len(trades) > 0:
        print(f"\n{model} ({len(trades)} trades):")
        for i, trade in enumerate(trades[:5], 1):  # Mostrar primeros 5
            print(f"  {i}. {trade['type']} @ ${trade['price']:,.2f} ({trade['timestamp']})")
        if len(trades) > 5:
            print(f"  ... y {len(trades) - 5} más")
    else:
        print(f"\n{model}: NO realizó trades (solo HOLD)")

# Beneficio ajustado al mercado (alpha)
print(f"\n[ALPHA] Beneficio ajustado al mercado:")
print("="*80)
print(f"Alpha = ROI_modelo - ROI_mercado")
print(f"(Mide habilidad del modelo independiente del mercado)\n")

for model, data in results.items():
    alpha = data['roi'] - hold_roi
    emoji = "[+]" if alpha > 0 else "[-]" if alpha < 0 else "[=]"
    print(f"{emoji} {model}:")
    print(f"    ROI Modelo: {data['roi']:+.2f}%")
    print(f"    ROI Mercado: {hold_roi:+.2f}%")
    print(f"    Alpha: {alpha:+.2f}pp")
    
    if alpha > 0:
        print(f"    CONCLUSIÓN: Modelo AÑADE valor (+{alpha:.2f}pp)")
    elif alpha < 0:
        print(f"    CONCLUSIÓN: Modelo DESTRUYE valor ({alpha:.2f}pp)")
    else:
        print(f"    CONCLUSIÓN: Modelo igual que mercado")
    print()

# Confidence Score
if 'Confidence_Score' in df.columns:
    print(f"\n[CONFIDENCE] Análisis de Confianza:")
    print("="*80)
    conf_data = df.groupby('Cycle').first()['Confidence_Score']
    print(f"  Confidence Promedio: {conf_data.mean():.1f}%")
    print(f"  Confidence Mediana: {conf_data.median():.1f}%")
    print(f"  Mínimo: {conf_data.min():.1f}%")
    print(f"  Máximo: {conf_data.max():.1f}%")
    
    high_conf = (conf_data >= 75).sum()
    total_cycles = len(conf_data)
    print(f"\n  Ciclos con Alta Confianza (≥75%): {high_conf}/{total_cycles} ({high_conf/total_cycles*100:.1f}%)")
    print(f"  Ciclos con Baja Confianza (<75%): {total_cycles-high_conf}/{total_cycles} ({(total_cycles-high_conf)/total_cycles*100:.1f}%)")

# Ranking final
print(f"\n[RANKING] Mejores Modelos:")
print("="*80)
sorted_models = sorted(results.items(), key=lambda x: x[1]['roi'], reverse=True)
for i, (model, data) in enumerate(sorted_models, 1):
    emoji = "[1st]" if i == 1 else "[2nd]" if i == 2 else "[3rd]" if i == 3 else "[4th]"
    alpha = data['roi'] - hold_roi
    print(f"{emoji} {model}:")
    print(f"     ROI: {data['roi']:+.2f}% | Alpha: {alpha:+.2f}pp | Trades: {data['num_trades']}")

print("\n" + "="*80)
print("[CONCLUSIÓN] RESUMEN EJECUTIVO")
print("="*80)

best_model = sorted_models[0][0]
best_roi = sorted_models[0][1]['roi']
best_alpha = best_roi - hold_roi

print(f"\n[MEJOR MODELO]: {best_model}")
print(f"  ROI: {best_roi:+.2f}%")
print(f"  Alpha: {best_alpha:+.2f}pp")
print(f"  Trades: {sorted_models[0][1]['num_trades']}")

print(f"\n[MERCADO]: {market_type} ({price_change:+.2f}%)")

if best_alpha > 0:
    print(f"\n[RECOMENDACIÓN]: {best_model} SUPERA al mercado en {best_alpha:.2f}pp")
    print(f"  ✓ Usar este modelo en producción")
elif best_roi > 0 and best_alpha <= 0:
    print(f"\n[RECOMENDACIÓN]: {best_model} tiene ganancias pero NO supera Hold")
    print(f"  → Considerar estrategia Buy & Hold simple")
else:
    print(f"\n[RECOMENDACIÓN]: Todos los modelos tienen pérdidas")
    if price_change < -2:
        print(f"  → Causa: Mercado bajista")
        print(f"  → Ejecutar en mercado alcista/neutral")
    else:
        print(f"  → Causa: Decisiones pobres de los modelos")
        print(f"  → Ajustar prompts o parámetros")

print("\n" + "="*80)
