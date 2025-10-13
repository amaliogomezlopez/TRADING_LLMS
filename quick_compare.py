"""
QUICK COMPARISON - Compara resultados de model_comparison.csv vs trading_log.csv
Permite ver si el sistema multi-modelo rinde mejor que un solo modelo
"""
import pandas as pd
import os
from datetime import datetime

def load_data():
    """Carga ambos archivos CSV."""
    data = {}
    
    # Model comparison data
    if os.path.exists('model_comparison.csv'):
        df_comp = pd.read_csv('model_comparison.csv')
        df_comp['Timestamp'] = pd.to_datetime(df_comp['Timestamp'])
        data['comparison'] = df_comp
        print(f"✅ Loaded model_comparison.csv: {len(df_comp)} records")
    else:
        print("❌ model_comparison.csv not found")
        data['comparison'] = None
    
    # Trading log data
    if os.path.exists('trading_log.csv'):
        df_log = pd.read_csv('trading_log.csv')
        df_log['Timestamp'] = pd.to_datetime(df_log['Timestamp'])
        data['trading'] = df_log
        print(f"✅ Loaded trading_log.csv: {len(df_log)} records")
    else:
        print("❌ trading_log.csv not found")
        data['trading'] = None
    
    return data

def compare_signal_distribution(data):
    """Compara la distribución de señales."""
    
    print("\n" + "="*80)
    print("📊 DISTRIBUCIÓN DE SEÑALES")
    print("="*80)
    
    # Trading bot (single model)
    if data['trading'] is not None:
        df_trading = data['trading']
        trading_signals = df_trading['Action'].value_counts()
        total_trading = len(df_trading)
        
        print("\n🤖 TRADING BOT (Llama-3.1-8B solo):")
        print(f"   Total: {total_trading} ciclos")
        for signal, count in trading_signals.items():
            pct = (count / total_trading * 100)
            print(f"   {signal}: {count} ({pct:.1f}%)")
    
    # Model comparison (consensus)
    if data['comparison'] is not None:
        df_comp = data['comparison']
        # Get consensus per cycle (first occurrence)
        consensus = df_comp.groupby('Cycle')['Consensus_Signal'].first()
        consensus_counts = consensus.value_counts()
        total_consensus = len(consensus)
        
        print(f"\n🤖 MODEL COMPARISON (Consenso de 4 modelos):")
        print(f"   Total: {total_consensus} ciclos")
        for signal, count in consensus_counts.items():
            pct = (count / total_consensus * 100)
            print(f"   {signal}: {count} ({pct:.1f}%)")
        
        # Average agreement
        avg_agreement = df_comp.groupby('Cycle')['Agreement_Level'].first().mean()
        print(f"\n   Nivel promedio de acuerdo: {avg_agreement:.1f}%")
    
    print("\n" + "="*80)

def compare_by_model(data):
    """Compara cada modelo vs el bot original."""
    
    if data['comparison'] is None:
        return
    
    print("\n" + "="*80)
    print("🔍 COMPARACIÓN POR MODELO vs BOT ORIGINAL")
    print("="*80)
    
    df_comp = data['comparison']
    models = df_comp['Model_Name'].unique()
    
    # Get trading bot distribution
    if data['trading'] is not None:
        df_trading = data['trading']
        trading_signals = df_trading['Action'].value_counts(normalize=True) * 100
        trading_buy = trading_signals.get('BUY', 0)
        trading_sell = trading_signals.get('SELL', 0)
        trading_hold = trading_signals.get('HOLD', 0)
        
        print(f"\n📊 Bot Original (Llama-3.1-8B):")
        print(f"   BUY: {trading_buy:.1f}% | SELL: {trading_sell:.1f}% | HOLD: {trading_hold:.1f}%")
        print("\n" + "-"*80)
    
    for model in models:
        model_df = df_comp[df_comp['Model_Name'] == model]
        signal_counts = model_df['Model_Signal'].value_counts(normalize=True) * 100
        
        buy_pct = signal_counts.get('BUY', 0)
        sell_pct = signal_counts.get('SELL', 0)
        hold_pct = signal_counts.get('HOLD', 0)
        
        print(f"\n🤖 {model}:")
        print(f"   BUY: {buy_pct:.1f}% | SELL: {sell_pct:.1f}% | HOLD: {hold_pct:.1f}%")
        
        # Difference from original
        if data['trading'] is not None:
            buy_diff = buy_pct - trading_buy
            sell_diff = sell_pct - trading_sell
            hold_diff = hold_pct - trading_hold
            
            print(f"   Diferencia: BUY {buy_diff:+.1f}% | SELL {sell_diff:+.1f}% | HOLD {hold_diff:+.1f}%")
    
    print("\n" + "="*80)

def time_overlap_analysis(data):
    """Analiza si hay períodos de tiempo que se solapan."""
    
    if data['comparison'] is None or data['trading'] is None:
        print("\n⚠️ No se pueden comparar períodos (falta algún archivo)")
        return
    
    print("\n" + "="*80)
    print("📅 ANÁLISIS DE PERÍODOS DE TIEMPO")
    print("="*80)
    
    df_trading = data['trading']
    df_comp = data['comparison']
    
    # Time ranges
    trading_start = df_trading['Timestamp'].min()
    trading_end = df_trading['Timestamp'].max()
    comp_start = df_comp['Timestamp'].min()
    comp_end = df_comp['Timestamp'].max()
    
    print(f"\n🤖 Bot Original:")
    print(f"   Desde: {trading_start}")
    print(f"   Hasta: {trading_end}")
    print(f"   Duración: {trading_end - trading_start}")
    
    print(f"\n🤖 Model Comparison:")
    print(f"   Desde: {comp_start}")
    print(f"   Hasta: {comp_end}")
    print(f"   Duración: {comp_end - comp_start}")
    
    # Check overlap
    if comp_start <= trading_end and comp_end >= trading_start:
        overlap_start = max(trading_start, comp_start)
        overlap_end = min(trading_end, comp_end)
        print(f"\n⚠️ HAY SOLAPAMIENTO:")
        print(f"   Desde: {overlap_start}")
        print(f"   Hasta: {overlap_end}")
        print(f"   Duración: {overlap_end - overlap_start}")
        print("\n   ⚠️ NOTA: Mismos datos de mercado, se pueden comparar directamente")
    else:
        print(f"\n✅ NO HAY SOLAPAMIENTO:")
        print("   Los datasets corresponden a períodos diferentes")
        print("   ⚠️ Comparación limitada (diferentes condiciones de mercado)")
    
    print("\n" + "="*80)

def consensus_quality(data):
    """Analiza la calidad del consenso."""
    
    if data['comparison'] is None:
        return
    
    print("\n" + "="*80)
    print("🎯 CALIDAD DEL CONSENSO")
    print("="*80)
    
    df_comp = data['comparison']
    
    # Agreement levels
    agreements = df_comp.groupby('Cycle')['Agreement_Level'].first()
    
    unanimous = (agreements == 100).sum()
    high_agreement = ((agreements >= 75) & (agreements < 100)).sum()
    medium_agreement = ((agreements >= 50) & (agreements < 75)).sum()
    low_agreement = (agreements < 50).sum()
    
    total = len(agreements)
    
    print(f"\n📊 Distribución de Nivel de Acuerdo:")
    print(f"   🎯 Unanimidad (100%):      {unanimous:3d} / {total} ({unanimous/total*100:5.1f}%)")
    print(f"   ✅ Alto (75-99%):           {high_agreement:3d} / {total} ({high_agreement/total*100:5.1f}%)")
    print(f"   ⚠️ Medio (50-74%):          {medium_agreement:3d} / {total} ({medium_agreement/total*100:5.1f}%)")
    print(f"   ❌ Bajo (<50%):             {low_agreement:3d} / {total} ({low_agreement/total*100:5.1f}%)")
    
    # Recommendation
    high_confidence = unanimous + high_agreement
    print(f"\n💡 RECOMENDACIÓN:")
    print(f"   Ciclos con alta confianza (≥75%): {high_confidence}/{total} ({high_confidence/total*100:.1f}%)")
    if high_confidence / total >= 0.7:
        print("   ✅ Sistema de consenso es CONFIABLE")
    elif high_confidence / total >= 0.5:
        print("   ⚠️ Sistema de consenso es MODERADAMENTE CONFIABLE")
    else:
        print("   ❌ Sistema de consenso tiene BAJA CONFIABILIDAD")
    
    print("\n" + "="*80)

def main():
    """Menu principal."""
    
    print("\n" + "="*80)
    print("⚡ QUICK COMPARISON - Bot Original vs Multi-Modelo")
    print("="*80)
    
    data = load_data()
    
    if data['comparison'] is None and data['trading'] is None:
        print("\n❌ No hay datos para analizar. Ejecuta primero:")
        print("   1. python trading_bot.py (para trading_log.csv)")
        print("   2. python model_comparison.py (para model_comparison.csv)")
        return
    
    print("\n1. Comparar distribución de señales")
    print("2. Comparar por modelo individual")
    print("3. Analizar períodos de tiempo")
    print("4. Calidad del consenso")
    print("5. Ver todo (reporte completo)")
    print("0. Salir")
    
    choice = input("\nSelecciona una opción: ").strip()
    
    if choice == '1':
        compare_signal_distribution(data)
    elif choice == '2':
        compare_by_model(data)
    elif choice == '3':
        time_overlap_analysis(data)
    elif choice == '4':
        consensus_quality(data)
    elif choice == '5':
        compare_signal_distribution(data)
        compare_by_model(data)
        time_overlap_analysis(data)
        consensus_quality(data)
    elif choice == '0':
        print("\n👋 ¡Hasta luego!")
    else:
        print("\n❌ Opción inválida")

if __name__ == "__main__":
    main()
