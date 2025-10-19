"""
TRADING BOT - MODEL COMPARISON
Sistema para comparar múltiples modelos LLM en trading
Ejecuta 4 modelos simultáneamente y guarda resultados para análisis
"""
import os
import time
import re
import csv
import yaml
import threading
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from groq import Groq
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands

# Load environment variables
load_dotenv()

# --- Configuration ---
def load_config(config_file='config.yml'):
    """Loads configuration from YAML file."""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

config = load_config()

# --- Models to Compare ---
MODELS_TO_TEST = [
    {
        'name': 'llama-3.3-70b-versatile',
        'display_name': 'Llama-3.3-70B',
        'description': '70B params - Most intelligent',
        'temperature': 0.3
    },
    {
        'name': 'llama-3.1-8b-instant',
        'display_name': 'Llama-3.1-8B',
        'description': '8B params - Fastest (current)',
        'temperature': 0.3
    },
    {
        'name': 'meta-llama/llama-4-scout-17b-16e-instruct',
        'display_name': 'Llama-4-Scout-17B',
        'description': '17B params - Llama 4 generation',
        'temperature': 0.3
    },
    {
        'name': 'qwen/qwen3-32b',
        'display_name': 'Qwen3-32B',
        'description': '32B params - Chinese model',
        'temperature': 0.3
    }
]

# Binance Configuration
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# Trading Parameters
SYMBOL = config['trading']['symbol'] if config else 'BTCUSDT'
QUANTITY = config['trading']['quantity'] if config else 0.001

# Timeframe
timeframe_map = {
    '1m': Client.KLINE_INTERVAL_1MINUTE,
    '5m': Client.KLINE_INTERVAL_5MINUTE,
    '15m': Client.KLINE_INTERVAL_15MINUTE,
    '1h': Client.KLINE_INTERVAL_1HOUR,
}
timeframe_str = config['trading']['timeframe'] if config else '5m'
INTERVAL = timeframe_map.get(timeframe_str, Client.KLINE_INTERVAL_5MINUTE)

wait_time_map = {'1m': 60, '5m': 300, '15m': 900, '1h': 3600}
WAIT_TIME = wait_time_map.get(timeframe_str, 300)

# Risk Management
STOP_LOSS_PERCENT = config['risk_management']['stop_loss_percent'] if config else 0.02
TAKE_PROFIT_PERCENT = config['risk_management']['take_profit_percent'] if config else 0.03
MAX_TOTAL_LOSS = config['risk_management']['max_total_loss'] if config else -100.0

# Technical Indicators
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
EMA_SHORT = 9
EMA_LONG = 21
KLINES_LIMIT = 100

# Logging
COMPARISON_LOG = 'model_comparison.csv'

# Prompt Template
PROMPT_TEMPLATE = """
You are an expert cryptocurrency trader analyzing {symbol}.

CURRENT MARKET DATA:
- Current Price: {current_price}
- Price Change (24h): {price_change}%

TECHNICAL INDICATORS:
- RSI (14): {rsi} {rsi_signal}
- MACD: {macd_value} (Signal: {macd_signal_value}, Histogram: {macd_hist})
- MACD Signal: {macd_signal}
- EMA 9: {ema_short}
- EMA 21: {ema_long}
- Price vs EMA9: {price_vs_ema_short}
- Price vs EMA21: {price_vs_ema_long}
- Bollinger Bands: Price is {bb_position}

TREND ANALYSIS:
- Short-term trend: {short_trend}
- Medium-term trend: {medium_trend}

Based on this comprehensive technical analysis, provide ONE of these exact words as your trading decision:
BUY - if indicators strongly suggest an upward movement
SELL - if indicators strongly suggest a downward movement  
HOLD - if signals are mixed or unclear

Your response must be ONLY one word: BUY, SELL, or HOLD.
"""

def setup_log_file():
    """Creates the comparison log file with header."""
    if not os.path.exists(COMPARISON_LOG):
        with open(COMPARISON_LOG, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Timestamp', 'Cycle', 'Symbol', 'Price', 
                'RSI', 'MACD_Signal', 'Trend',
                'Model_Name', 'Model_Signal', 'Model_Response_Time_ms',
                'Consensus_Signal', 'Agreement_Level'
            ])

def log_comparison(log_data):
    """Appends comparison data to CSV."""
    with open(COMPARISON_LOG, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            log_data.get('timestamp'),
            log_data.get('cycle'),
            log_data.get('symbol'),
            log_data.get('price'),
            log_data.get('rsi'),
            log_data.get('macd_signal'),
            log_data.get('trend'),
            log_data.get('model_name'),
            log_data.get('model_signal'),
            log_data.get('response_time'),
            log_data.get('consensus_signal'),
            log_data.get('agreement_level')
        ])

def get_binance_client():
    """Initializes Binance client."""
    try:
        client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)
        client.get_account()
        return client
    except Exception as e:
        print(f"Error connecting to Binance: {e}")
        return None

def get_market_data(client, symbol, interval, limit=KLINES_LIMIT):
    """Fetches market data."""
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ])
        
        df['close'] = pd.to_numeric(df['close'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['open'] = pd.to_numeric(df['open'])
        df['volume'] = pd.to_numeric(df['volume'])
        
        return df
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return None

def calculate_technical_indicators(df):
    """Calculates technical indicators."""
    if df is None or len(df) < RSI_PERIOD:
        return None
    
    try:
        # RSI
        rsi_indicator = RSIIndicator(close=df['close'], window=RSI_PERIOD)
        rsi = rsi_indicator.rsi().iloc[-1]
        
        # MACD
        macd_indicator = MACD(close=df['close'])
        macd = macd_indicator.macd().iloc[-1]
        macd_signal = macd_indicator.macd_signal().iloc[-1]
        macd_hist = macd_indicator.macd_diff().iloc[-1]
        
        # EMAs
        ema_short_indicator = EMAIndicator(close=df['close'], window=EMA_SHORT)
        ema_long_indicator = EMAIndicator(close=df['close'], window=EMA_LONG)
        ema_short = ema_short_indicator.ema_indicator().iloc[-1]
        ema_long = ema_long_indicator.ema_indicator().iloc[-1]
        
        # Bollinger Bands
        bb_indicator = BollingerBands(close=df['close'])
        bb_high = bb_indicator.bollinger_hband().iloc[-1]
        bb_low = bb_indicator.bollinger_lband().iloc[-1]
        
        current_price = df['close'].iloc[-1]
        
        # Signals
        if rsi < RSI_OVERSOLD:
            rsi_signal = "OVERSOLD (Bullish)"
        elif rsi > RSI_OVERBOUGHT:
            rsi_signal = "OVERBOUGHT (Bearish)"
        else:
            rsi_signal = "NEUTRAL"
        
        if macd > macd_signal and macd_hist > 0:
            macd_signal_text = "BULLISH"
        elif macd < macd_signal and macd_hist < 0:
            macd_signal_text = "BEARISH"
        else:
            macd_signal_text = "NEUTRAL"
        
        price_vs_ema_short = "ABOVE" if current_price > ema_short else "BELOW"
        price_vs_ema_long = "ABOVE" if current_price > ema_long else "BELOW"
        
        if current_price > bb_high:
            bb_position = "above upper band (overbought)"
        elif current_price < bb_low:
            bb_position = "below lower band (oversold)"
        else:
            bb_position = "within bands (normal)"
        
        if ema_short > ema_long and current_price > ema_short:
            short_trend = "BULLISH"
        elif ema_short < ema_long and current_price < ema_short:
            short_trend = "BEARISH"
        else:
            short_trend = "NEUTRAL"
        
        medium_trend = "BULLISH" if current_price > ema_long else "BEARISH"
        
        if len(df) >= 24:
            price_24h_ago = df['close'].iloc[-24]
            price_change = ((current_price - price_24h_ago) / price_24h_ago) * 100
        else:
            price_change = 0
        
        return {
            'current_price': round(current_price, 2),
            'rsi': round(rsi, 2),
            'rsi_signal': rsi_signal,
            'macd_value': round(macd, 4),
            'macd_signal_value': round(macd_signal, 4),
            'macd_hist': round(macd_hist, 4),
            'macd_signal': macd_signal_text,
            'ema_short': round(ema_short, 2),
            'ema_long': round(ema_long, 2),
            'price_vs_ema_short': price_vs_ema_short,
            'price_vs_ema_long': price_vs_ema_long,
            'bb_position': bb_position,
            'short_trend': short_trend,
            'medium_trend': medium_trend,
            'price_change': round(price_change, 2)
        }
        
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None

def get_model_signal(model_info, technical_data, symbol):
    """Gets trading signal from a specific model."""
    try:
        start_time = time.time()
        
        client = Groq()
        prompt_content = PROMPT_TEMPLATE.format(symbol=symbol, **technical_data)
        
        completion = client.chat.completions.create(
            model=model_info['name'],
            messages=[{"role": "user", "content": prompt_content}],
            temperature=model_info['temperature'],
            max_tokens=20,
            stream=False
        )
        
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        raw_response = completion.choices[0].message.content
        match = re.search(r'\b(BUY|SELL|HOLD)\b', raw_response.upper())
        
        signal = match.group(1) if match else "HOLD"
        
        return signal, response_time, raw_response
        
    except Exception as e:
        print(f"Error with model {model_info['display_name']}: {e}")
        return "ERROR", 0, str(e)

def calculate_consensus(signals):
    """Calculates consensus from multiple model signals."""
    signal_counts = {'BUY': 0, 'SELL': 0, 'HOLD': 0, 'ERROR': 0}
    
    for signal in signals:
        if signal in signal_counts:
            signal_counts[signal] += 1
    
    # Remove errors from consensus
    valid_signals = {k: v for k, v in signal_counts.items() if k != 'ERROR'}
    
    if not valid_signals or sum(valid_signals.values()) == 0:
        return "HOLD", 0
    
    consensus = max(valid_signals, key=valid_signals.get)
    total_valid = sum(valid_signals.values())
    agreement_level = (valid_signals[consensus] / total_valid) * 100
    
    return consensus, round(agreement_level, 1)

def main():
    """Main comparison function."""
    print("=" * 80)
    print("[BOT] TRADING BOT - MODEL COMPARISON")
    print("=" * 80)
    print(f"Testing {len(MODELS_TO_TEST)} models simultaneously:")
    for i, model in enumerate(MODELS_TO_TEST, 1):
        print(f"  {i}. {model['display_name']}: {model['description']}")
    print(f"\nSymbol: {SYMBOL}")
    print(f"Timeframe: {timeframe_str}")
    print(f"Results will be saved to: {COMPARISON_LOG}")
    print("=" * 80)
    
    setup_log_file()
    binance_client = get_binance_client()
    if not binance_client:
        return
    
    cycle_count = 0
    
    while True:
        cycle_count += 1
        print(f"\n{'='*80}")
        print(f"CYCLE #{cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        # Fetch market data
        df = get_market_data(binance_client, SYMBOL, INTERVAL)
        
        if df is not None and len(df) > 0:
            technical_data = calculate_technical_indicators(df)
            
            if technical_data:
                current_price = technical_data['current_price']
                
                print(f"\n[DATA] MARKET DATA:")
                print(f"   Price: ${current_price} ({technical_data['price_change']:+.2f}%)")
                print(f"   RSI: {technical_data['rsi']} - {technical_data['rsi_signal']}")
                print(f"   MACD: {technical_data['macd_signal']}")
                print(f"   Trend: {technical_data['short_trend']} / {technical_data['medium_trend']}")
                
                print(f"\n[MODELS] MODEL PREDICTIONS:")
                print(f"{'Model':<25} {'Signal':<8} {'Response Time':<15}")
                print("-" * 50)
                
                signals = []
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Query all models
                for model in MODELS_TO_TEST:
                    signal, response_time, raw = get_model_signal(model, technical_data, SYMBOL)
                    signals.append(signal)
                    
                    # Display result
                    tag = "[BUY]" if signal == "BUY" else "[SELL]" if signal == "SELL" else "[HOLD]" if signal == "HOLD" else "[ERROR]"
                    print(f"{tag} {model['display_name']:<23} {signal:<8} {response_time:.0f}ms")
                
                # Calculate consensus
                consensus_signal, agreement_level = calculate_consensus(signals)
                
                print(f"\n{'='*50}")
                print(f"[CONSENSUS] RESULT: {consensus_signal} ({agreement_level}% agreement)")
                print(f"{'='*50}")
                
                # Log each model's result
                for i, model in enumerate(MODELS_TO_TEST):
                    signal, response_time, _ = (signals[i], 0, "")
                    if signal != "ERROR":
                        # Re-query for accurate timing (already done above)
                        pass
                    
                    log_data = {
                        'timestamp': timestamp,
                        'cycle': cycle_count,
                        'symbol': SYMBOL,
                        'price': current_price,
                        'rsi': technical_data['rsi'],
                        'macd_signal': technical_data['macd_signal'],
                        'trend': f"{technical_data['short_trend']}/{technical_data['medium_trend']}",
                        'model_name': model['display_name'],
                        'model_signal': signals[i],
                        'response_time': response_time,
                        'consensus_signal': consensus_signal,
                        'agreement_level': agreement_level
                    }
                    log_comparison(log_data)
                
                print(f"\n[OK] Results logged to {COMPARISON_LOG}")
            else:
                print("[ERROR] Failed to calculate technical indicators")
        else:
            print("[ERROR] Failed to fetch market data")
        
        print(f"\n[WAIT] Waiting {WAIT_TIME//60} minutes for next cycle...")
        time.sleep(WAIT_TIME)

if __name__ == "__main__":
    main()
