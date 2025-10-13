"""
Script para analizar el performance del trading bot
"""
import pandas as pd
import os

LOG_FILE = 'trading_log.csv'

def analyze_trading_log():
    """Analiza el log de trading y muestra estadísticas."""
    
    if not os.path.exists(LOG_FILE):
        print(f"❌ Archivo {LOG_FILE} no encontrado.")
        return
    
    # Leer CSV
    df = pd.read_csv(LOG_FILE)
    
    if len(df) == 0:
        print("❌ El log está vacío.")
        return
    
    print("=" * 60)
    print("📊 ANÁLISIS DEL TRADING BOT")
    print("=" * 60)
    
    # Información general
    print(f"\n📅 PERÍODO:")
    print(f"   Primer registro: {df['Timestamp'].iloc[0]}")
    print(f"   Último registro: {df['Timestamp'].iloc[-1]}")
    print(f"   Total de ciclos: {len(df)}")
    
    # Análisis de señales
    print(f"\n🤖 SEÑALES DEL LLM:")
    signal_counts = df['LLM_Signal'].value_counts()
    for signal, count in signal_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   {signal}: {count} ({percentage:.1f}%)")
    
    # Análisis de acciones
    print(f"\n⚡ ACCIONES EJECUTADAS:")
    action_counts = df['Action_Taken'].value_counts()
    for action, count in action_counts.items():
        print(f"   {action}: {count}")
    
    # Trades ejecutados
    buys = df[df['Action_Taken'] == 'BUY']
    sells = df[df['Action_Taken'].str.contains('SELL', na=False)]
    
    print(f"\n💰 TRADES:")
    print(f"   Compras (BUY): {len(buys)}")
    print(f"   Ventas (SELL): {len(sells)}")
    
    # P&L Analysis
    if 'Trade_PNL' in df.columns:
        completed_trades = df[df['Trade_PNL'].notna()]
        
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
                print(f"   Average ganancia: ${avg_win:.2f}")
            
            if len(losing_trades) > 0:
                avg_loss = losing_trades['Trade_PNL'].mean()
                print(f"   Average pérdida: ${avg_loss:.2f}")
            
            # Risk metrics
            if len(winning_trades) > 0 and len(losing_trades) > 0:
                profit_factor = abs(winning_trades['Trade_PNL'].sum() / losing_trades['Trade_PNL'].sum())
                print(f"\n📊 MÉTRICAS DE RIESGO:")
                print(f"   Profit Factor: {profit_factor:.2f}")
    
    # Technical indicators analysis
    if 'RSI' in df.columns and df['RSI'].notna().any():
        print(f"\n🔧 INDICADORES TÉCNICOS (Promedios):")
        avg_rsi = df['RSI'].dropna().mean()
        print(f"   RSI Promedio: {avg_rsi:.2f}")
        
        # RSI distribution
        oversold = len(df[df['RSI'] < 30])
        overbought = len(df[df['RSI'] > 70])
        neutral = len(df[(df['RSI'] >= 30) & (df['RSI'] <= 70)])
        
        print(f"\n   Distribución RSI:")
        print(f"      Oversold (<30): {oversold}")
        print(f"      Neutral (30-70): {neutral}")
        print(f"      Overbought (>70): {overbought}")
    
    # Latest status
    latest = df.iloc[-1]
    print(f"\n📌 ÚLTIMO ESTADO:")
    print(f"   Señal: {latest['LLM_Signal']}")
    print(f"   Acción: {latest['Action_Taken']}")
    if pd.notna(latest.get('Total_PNL')):
        print(f"   Total P&L: ${latest['Total_PNL']:.2f}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    analyze_trading_log()
