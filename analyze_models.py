"""
MODEL COMPARISON ANALYZER
Analiza el rendimiento de diferentes modelos LLM en trading
"""
import pandas as pd
import os
from datetime import datetime, timedelta

COMPARISON_LOG = 'model_comparison.csv'

def analyze_models(hours=None):
    """Analiza el rendimiento de cada modelo."""
    
    if not os.path.exists(COMPARISON_LOG):
        print(f"❌ No se encontró el archivo {COMPARISON_LOG}")
        return
    
    # Load data
    df = pd.read_csv(COMPARISON_LOG)
    
    if df.empty:
        print("⚠️ No hay datos para analizar")
        return
    
    # Convert timestamp
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Filter by time period if specified
    if hours:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        df = df[df['Timestamp'] >= cutoff_time]
        print(f"📊 Analizando últimas {hours} horas ({len(df)} registros)")
    else:
        print(f"📊 Analizando todos los datos ({len(df)} registros)")
    
    if df.empty:
        print("⚠️ No hay datos en el período seleccionado")
        return
    
    print(f"\n{'='*80}")
    print("🤖 COMPARACIÓN DE MODELOS LLM")
    print(f"{'='*80}")
    
    # Group by model
    models = df['Model_Name'].unique()
    
    print(f"\nModelos analizados: {len(models)}")
    print(f"Período: {df['Timestamp'].min()} a {df['Timestamp'].max()}")
    print(f"Total ciclos: {df['Cycle'].nunique()}")
    
    # Analysis per model
    print(f"\n{'='*80}")
    print("📈 ESTADÍSTICAS POR MODELO")
    print(f"{'='*80}\n")
    
    results = []
    
    for model in models:
        model_df = df[df['Model_Name'] == model]
        
        # Signal distribution
        signal_counts = model_df['Model_Signal'].value_counts()
        total_signals = len(model_df)
        
        buy_pct = (signal_counts.get('BUY', 0) / total_signals * 100) if total_signals > 0 else 0
        sell_pct = (signal_counts.get('SELL', 0) / total_signals * 100) if total_signals > 0 else 0
        hold_pct = (signal_counts.get('HOLD', 0) / total_signals * 100) if total_signals > 0 else 0
        error_pct = (signal_counts.get('ERROR', 0) / total_signals * 100) if total_signals > 0 else 0
        
        # Response time
        avg_response_time = model_df['Model_Response_Time_ms'].mean()
        
        # Agreement with consensus
        consensus_match = (model_df['Model_Signal'] == model_df['Consensus_Signal']).sum()
        agreement_rate = (consensus_match / total_signals * 100) if total_signals > 0 else 0
        
        # Aggressiveness (BUY + SELL vs HOLD)
        aggressive_signals = signal_counts.get('BUY', 0) + signal_counts.get('SELL', 0)
        aggressiveness = (aggressive_signals / total_signals * 100) if total_signals > 0 else 0
        
        results.append({
            'model': model,
            'total_signals': total_signals,
            'buy_pct': buy_pct,
            'sell_pct': sell_pct,
            'hold_pct': hold_pct,
            'error_pct': error_pct,
            'avg_response_ms': avg_response_time,
            'consensus_agreement': agreement_rate,
            'aggressiveness': aggressiveness
        })
        
        print(f"🤖 {model}")
        print(f"   Total señales: {total_signals}")
        print(f"   BUY:  {signal_counts.get('BUY', 0):3d} ({buy_pct:5.1f}%)")
        print(f"   SELL: {signal_counts.get('SELL', 0):3d} ({sell_pct:5.1f}%)")
        print(f"   HOLD: {signal_counts.get('HOLD', 0):3d} ({hold_pct:5.1f}%)")
        if signal_counts.get('ERROR', 0) > 0:
            print(f"   ⚠️ ERROR: {signal_counts.get('ERROR', 0):3d} ({error_pct:5.1f}%)")
        print(f"   Tiempo respuesta: {avg_response_time:.0f}ms")
        print(f"   Acuerdo con consenso: {agreement_rate:.1f}%")
        print(f"   Agresividad (BUY+SELL): {aggressiveness:.1f}%")
        print()
    
    # Rankings
    print(f"\n{'='*80}")
    print("🏆 RANKINGS")
    print(f"{'='*80}\n")
    
    results_df = pd.DataFrame(results)
    
    # 1. Fastest
    print("⚡ MÁS RÁPIDO (menor tiempo de respuesta):")
    fastest = results_df.nsmallest(4, 'avg_response_ms')
    for i, row in fastest.iterrows():
        print(f"   {row['model']}: {row['avg_response_ms']:.0f}ms")
    
    # 2. Most consensus agreement
    print("\n🤝 MAYOR ACUERDO CON CONSENSO:")
    most_agreed = results_df.nlargest(4, 'consensus_agreement')
    for i, row in most_agreed.iterrows():
        print(f"   {row['model']}: {row['consensus_agreement']:.1f}%")
    
    # 3. Most aggressive
    print("\n⚔️ MÁS AGRESIVO (más BUY+SELL):")
    most_aggressive = results_df.nlargest(4, 'aggressiveness')
    for i, row in most_aggressive.iterrows():
        print(f"   {row['model']}: {row['aggressiveness']:.1f}%")
    
    # 4. Most conservative
    print("\n🛡️ MÁS CONSERVADOR (más HOLD):")
    most_conservative = results_df.nlargest(4, 'hold_pct')
    for i, row in most_conservative.iterrows():
        print(f"   {row['model']}: {row['hold_pct']:.1f}% HOLD")
    
    # Consensus analysis
    print(f"\n{'='*80}")
    print("📊 ANÁLISIS DE CONSENSO")
    print(f"{'='*80}\n")
    
    consensus_counts = df.groupby('Cycle')['Consensus_Signal'].first().value_counts()
    total_cycles = df['Cycle'].nunique()
    
    print(f"Total decisiones de consenso: {total_cycles}")
    for signal, count in consensus_counts.items():
        pct = (count / total_cycles * 100)
        print(f"   {signal}: {count} ({pct:.1f}%)")
    
    # Average agreement level
    avg_agreement = df.groupby('Cycle')['Agreement_Level'].first().mean()
    print(f"\nNivel promedio de acuerdo: {avg_agreement:.1f}%")
    
    # Disagreement cases
    low_agreement = df[df['Agreement_Level'] < 50]['Cycle'].nunique()
    if low_agreement > 0:
        print(f"⚠️ Ciclos con bajo acuerdo (<50%): {low_agreement}")
    
    print(f"\n{'='*80}")

def compare_signal_patterns():
    """Analiza patrones de señales entre modelos."""
    
    if not os.path.exists(COMPARISON_LOG):
        print(f"❌ No se encontró el archivo {COMPARISON_LOG}")
        return
    
    df = pd.read_csv(COMPARISON_LOG)
    
    if df.empty:
        print("⚠️ No hay datos para analizar")
        return
    
    print(f"\n{'='*80}")
    print("🔍 PATRONES DE SEÑALES")
    print(f"{'='*80}\n")
    
    # Pivot table: Cycle x Model
    pivot = df.pivot_table(
        index='Cycle',
        columns='Model_Name',
        values='Model_Signal',
        aggfunc='first'
    )
    
    # Find unanimous decisions
    unanimous = []
    for cycle in pivot.index:
        signals = pivot.loc[cycle].dropna().unique()
        if len(signals) == 1:
            unanimous.append((cycle, signals[0]))
    
    if unanimous:
        print(f"✅ Decisiones unánimes: {len(unanimous)}/{len(pivot)} ciclos")
        print(f"   Distribución:")
        unanimous_signals = pd.Series([sig for _, sig in unanimous]).value_counts()
        for signal, count in unanimous_signals.items():
            print(f"      {signal}: {count}")
    else:
        print("⚠️ No hay decisiones unánimes")
    
    # Find maximum disagreement
    max_disagreement = []
    for cycle in pivot.index:
        signals = pivot.loc[cycle].dropna()
        unique_signals = signals.nunique()
        if unique_signals >= 3:  # BUY, SELL, HOLD all present
            max_disagreement.append(cycle)
    
    if max_disagreement:
        print(f"\n⚠️ Máximo desacuerdo (3+ señales diferentes): {len(max_disagreement)} ciclos")
        print(f"   Ciclos: {max_disagreement[:5]}{'...' if len(max_disagreement) > 5 else ''}")
    
    print()

def export_summary():
    """Exporta un resumen detallado a CSV."""
    
    if not os.path.exists(COMPARISON_LOG):
        print(f"❌ No se encontró el archivo {COMPARISON_LOG}")
        return
    
    df = pd.read_csv(COMPARISON_LOG)
    
    if df.empty:
        print("⚠️ No hay datos para exportar")
        return
    
    # Create summary by model
    models = df['Model_Name'].unique()
    summary_data = []
    
    for model in models:
        model_df = df[df['Model_Name'] == model]
        
        signal_counts = model_df['Model_Signal'].value_counts()
        total_signals = len(model_df)
        
        summary_data.append({
            'Model': model,
            'Total_Signals': total_signals,
            'BUY_Count': signal_counts.get('BUY', 0),
            'SELL_Count': signal_counts.get('SELL', 0),
            'HOLD_Count': signal_counts.get('HOLD', 0),
            'ERROR_Count': signal_counts.get('ERROR', 0),
            'BUY_Percent': (signal_counts.get('BUY', 0) / total_signals * 100) if total_signals > 0 else 0,
            'SELL_Percent': (signal_counts.get('SELL', 0) / total_signals * 100) if total_signals > 0 else 0,
            'HOLD_Percent': (signal_counts.get('HOLD', 0) / total_signals * 100) if total_signals > 0 else 0,
            'Avg_Response_Time_ms': model_df['Model_Response_Time_ms'].mean(),
            'Consensus_Agreement_Pct': ((model_df['Model_Signal'] == model_df['Consensus_Signal']).sum() / total_signals * 100) if total_signals > 0 else 0,
        })
    
    summary_df = pd.DataFrame(summary_data)
    output_file = 'model_summary.csv'
    summary_df.to_csv(output_file, index=False)
    
    print(f"✅ Resumen exportado a: {output_file}")

def main():
    """Menu principal."""
    print("\n" + "="*80)
    print("🤖 ANÁLISIS DE MODELOS LLM - TRADING")
    print("="*80)
    print("\n1. Analizar todos los datos")
    print("2. Analizar últimas 2 horas")
    print("3. Analizar últimas 6 horas")
    print("4. Analizar últimas 24 horas")
    print("5. Ver patrones de señales")
    print("6. Exportar resumen a CSV")
    print("0. Salir")
    
    choice = input("\nSelecciona una opción: ").strip()
    
    if choice == '1':
        analyze_models()
    elif choice == '2':
        analyze_models(hours=2)
    elif choice == '3':
        analyze_models(hours=6)
    elif choice == '4':
        analyze_models(hours=24)
    elif choice == '5':
        compare_signal_patterns()
    elif choice == '6':
        export_summary()
    elif choice == '0':
        print("👋 ¡Hasta luego!")
    else:
        print("❌ Opción inválida")

if __name__ == "__main__":
    main()
