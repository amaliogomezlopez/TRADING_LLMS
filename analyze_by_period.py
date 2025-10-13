"""
Script para analizar el performance del trading bot por períodos específicos
"""
import pandas as pd
import os
from datetime import datetime, timedelta

LOG_FILE = 'trading_log.csv'

def analyze_by_period(hours=None, from_datetime=None):
    """Analiza el log filtrado por período de tiempo."""
    
    if not os.path.exists(LOG_FILE):
        print(f"❌ Archivo {LOG_FILE} no encontrado.")
        return
    
    # Leer CSV
    df = pd.read_csv(LOG_FILE)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    if len(df) == 0:
        print("❌ El log está vacío.")
        return
    
    # Filtrar por período
    if hours:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        df_filtered = df[df['Timestamp'] >= cutoff_time]
        period_desc = f"últimas {hours} horas"
    elif from_datetime:
        df_filtered = df[df['Timestamp'] >= from_datetime]
        period_desc = f"desde {from_datetime}"
    else:
        df_filtered = df
        period_desc = "todo el período"
    
    if len(df_filtered) == 0:
        print(f"❌ No hay datos para {period_desc}.")
        return
    
    print("=" * 70)
    print(f"📊 ANÁLISIS DEL TRADING BOT - {period_desc.upper()}")
    print("=" * 70)
    
    # Información general
    print(f"\n📅 PERÍODO:")
    print(f"   Primer registro: {df_filtered['Timestamp'].iloc[0]}")
    print(f"   Último registro: {df_filtered['Timestamp'].iloc[-1]}")
    print(f"   Total de ciclos: {len(df_filtered)}")
    duration = df_filtered['Timestamp'].iloc[-1] - df_filtered['Timestamp'].iloc[0]
    print(f"   Duración: {duration}")
    
    # Análisis de señales
    print(f"\n🤖 SEÑALES DEL LLM:")
    signal_counts = df_filtered['LLM_Signal'].value_counts()
    for signal, count in signal_counts.items():
        percentage = (count / len(df_filtered)) * 100
        print(f"   {signal}: {count} ({percentage:.1f}%)")
    
    # Análisis de acciones
    print(f"\n⚡ ACCIONES EJECUTADAS:")
    action_counts = df_filtered['Action_Taken'].value_counts()
    for action, count in action_counts.items():
        print(f"   {action}: {count}")
    
    # Trades ejecutados
    buys = df_filtered[df_filtered['Action_Taken'] == 'BUY']
    sells = df_filtered[df_filtered['Action_Taken'].str.contains('SELL', na=False)]
    
    print(f"\n💰 TRADES:")
    print(f"   Compras (BUY): {len(buys)}")
    print(f"   Ventas (SELL): {len(sells)}")
    
    # P&L Analysis
    if 'Trade_PNL' in df_filtered.columns:
        completed_trades = df_filtered[df_filtered['Trade_PNL'].notna()]
        
        if len(completed_trades) > 0:
            print(f"\n📈 PERFORMANCE:")
            print(f"   Trades completados: {len(completed_trades)}")
            
            winning_trades = completed_trades[completed_trades['Trade_PNL'] > 0]
            losing_trades = completed_trades[completed_trades['Trade_PNL'] < 0]
            
            print(f"   Trades ganadores: {len(winning_trades)}")
            print(f"   Trades perdedores: {len(losing_trades)}")
            
            if len(completed_trades) > 0:
                win_rate = (len(winning_trades) / len(completed_trades)) * 100
                print(f"   Win Rate: {win_rate:.1f}%")
            
            total_pnl = completed_trades['Trade_PNL'].sum()
            avg_pnl = completed_trades['Trade_PNL'].mean()
            
            print(f"\n💵 P&L:")
            print(f"   Total P&L: ${total_pnl:.2f}")
            print(f"   Average P&L por trade: ${avg_pnl:.2f}")
            
            if len(winning_trades) > 0:
                avg_win = winning_trades['Trade_PNL'].mean()
                max_win = winning_trades['Trade_PNL'].max()
                print(f"   Average ganancia: ${avg_win:.2f}")
                print(f"   Máxima ganancia: ${max_win:.2f}")
            
            if len(losing_trades) > 0:
                avg_loss = losing_trades['Trade_PNL'].mean()
                max_loss = losing_trades['Trade_PNL'].min()
                print(f"   Average pérdida: ${avg_loss:.2f}")
                print(f"   Máxima pérdida: ${max_loss:.2f}")
            
            # Risk metrics
            if len(winning_trades) > 0 and len(losing_trades) > 0:
                profit_factor = abs(winning_trades['Trade_PNL'].sum() / losing_trades['Trade_PNL'].sum())
                print(f"\n📊 MÉTRICAS DE RIESGO:")
                print(f"   Profit Factor: {profit_factor:.2f}")
    
    # Technical indicators analysis
    if 'RSI' in df_filtered.columns and df_filtered['RSI'].notna().any():
        print(f"\n🔧 INDICADORES TÉCNICOS:")
        avg_rsi = df_filtered['RSI'].dropna().mean()
        print(f"   RSI Promedio: {avg_rsi:.2f}")
        
        # RSI distribution
        oversold = len(df_filtered[df_filtered['RSI'] < 30])
        overbought = len(df_filtered[df_filtered['RSI'] > 70])
        neutral = len(df_filtered[(df_filtered['RSI'] >= 30) & (df_filtered['RSI'] <= 70)])
        
        if oversold + overbought + neutral > 0:
            print(f"   Distribución RSI:")
            print(f"      Oversold (<30): {oversold}")
            print(f"      Neutral (30-70): {neutral}")
            print(f"      Overbought (>70): {overbought}")
    
    # Latest status
    latest = df_filtered.iloc[-1]
    print(f"\n📌 ÚLTIMO ESTADO:")
    print(f"   Timestamp: {latest['Timestamp']}")
    print(f"   Señal: {latest['LLM_Signal']}")
    print(f"   Acción: {latest['Action_Taken']}")
    if pd.notna(latest.get('Total_PNL')):
        print(f"   Total P&L: ${latest['Total_PNL']:.2f}")
    
    print("\n" + "=" * 70)
    
    return df_filtered

def compare_periods():
    """Compara diferentes períodos de tiempo."""
    print("\n🔄 COMPARACIÓN DE PERÍODOS\n")
    
    periods = [
        ("Última hora", 1),
        ("Últimas 2 horas", 2),
        ("Últimas 4 horas", 4),
        ("Últimas 8 horas", 8),
        ("Todo el tiempo", None)
    ]
    
    results = []
    
    for name, hours in periods:
        df = pd.read_csv(LOG_FILE)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        if hours:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            df_period = df[df['Timestamp'] >= cutoff_time]
        else:
            df_period = df
        
        if len(df_period) == 0:
            continue
        
        completed = df_period[df_period['Trade_PNL'].notna()]
        
        if len(completed) > 0:
            total_pnl = completed['Trade_PNL'].sum()
            win_rate = (len(completed[completed['Trade_PNL'] > 0]) / len(completed)) * 100
            trades = len(completed)
        else:
            total_pnl = 0
            win_rate = 0
            trades = 0
        
        results.append({
            'Período': name,
            'Ciclos': len(df_period),
            'Trades': trades,
            'Win Rate': f"{win_rate:.1f}%",
            'P&L': f"${total_pnl:.2f}"
        })
    
    if results:
        results_df = pd.DataFrame(results)
        print(results_df.to_string(index=False))

if __name__ == "__main__":
    import sys
    
    print("🔍 ANÁLISIS POR PERÍODOS")
    print("=" * 70)
    
    if len(sys.argv) > 1:
        try:
            hours = int(sys.argv[1])
            analyze_by_period(hours=hours)
        except ValueError:
            print("❌ Argumento inválido. Usa: python analyze_by_period.py <horas>")
    else:
        print("\n1️⃣ Análisis de las últimas 2 horas:")
        analyze_by_period(hours=2)
        
        print("\n\n2️⃣ Comparación de períodos:")
        compare_periods()
