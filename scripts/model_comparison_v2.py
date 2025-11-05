"""
TRADING BOT - MODEL COMPARISON V2 (OPTIMIZED)
Sistema mejorado con 4 nuevos modelos + gestión de riesgo avanzada
Incluye: Stop-Loss, Take-Profit, Trailing Stop, y contexto extendido para LLMs
"""
import os
import time
import re
import csv
import yaml
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from groq import Groq
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import MACD, EMAIndicator, ADXIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator, VolumeWeightedAveragePrice

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
        print(f"[ERROR] Loading config: {e}")
        return None

config = load_config()

# --- NEW Models V2 (Different from V1) ---
MODELS_V2 = [
    {
        'name': 'qwen/qwen3-32b',
        'display_name': 'Qwen3-32B',
        'description': '32B params - Prudent winner from V1',
        'temperature': 0.2,  # Lower temperature for more conservative
        'rpm': 60
    },
    {
        'name': 'meta-llama/llama-4-maverick-17b-128e-instruct',
        'display_name': 'Llama-4-Maverick-17B',
        'description': '17B params - Llama 4 Maverick variant',
        'temperature': 0.3,
        'rpm': 30
    },
    {
        'name': 'openai/gpt-oss-120b',
        'display_name': 'GPT-OSS-120B',
        'description': '120B params - Largest available model',
        'temperature': 0.25,
        'rpm': 30
    },
    {
        'name': 'moonshotai/kimi-k2-instruct',
        'display_name': 'Kimi-K2',
        'description': 'MoonShot AI - Alternative architecture',
        'temperature': 0.3,
        'rpm': 60
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

# ENHANCED Risk Management
STOP_LOSS_PERCENT = 0.02  # 2% stop loss
TAKE_PROFIT_PERCENT = 0.04  # 4% take profit (risk/reward 1:2)
TRAILING_STOP_PERCENT = 0.015  # 1.5% trailing stop
MAX_POSITION_SIZE = 0.1  # Max BTC per trade
CONFIDENCE_THRESHOLD = 75  # Min consensus % to trade

# Technical Indicators Periods
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
STOCH_PERIOD = 14
EMA_SHORT = 9
EMA_MEDIUM = 21
EMA_LONG = 50
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
ADX_PERIOD = 14
ATR_PERIOD = 14
KLINES_LIMIT = 200  # More data for better analysis

# Logging
COMPARISON_LOG_V2 = 'model_comparison_v2.csv'

# ENHANCED Prompt Template with More Context
PROMPT_TEMPLATE_V2 = """
You are an expert cryptocurrency trading algorithm analyzing {symbol} with advanced technical analysis.

=== CURRENT MARKET DATA ===
Price: ${current_price}
24h Change: {price_change}%
Volume 24h: ${volume_24h}
Price vs 24h Avg: {price_vs_avg}%

=== TREND INDICATORS ===
• EMA 9: ${ema_short} - Price is {price_vs_ema_short}
• EMA 21: ${ema_medium} - Price is {price_vs_ema_medium}
• EMA 50: ${ema_long} - Price is {price_vs_ema_long}
• EMA Alignment: {ema_alignment}
• Short-term Trend: {short_trend}
• Medium-term Trend: {medium_trend}
• Long-term Trend: {long_trend}
• Trend Strength (ADX): {adx_value} - {adx_signal}

=== MOMENTUM INDICATORS ===
• RSI (14): {rsi_value} - {rsi_signal}
• Stochastic: {stoch_k} - {stoch_signal}
• MACD: {macd_value} (Signal: {macd_signal_value})
• MACD Histogram: {macd_hist} - {macd_signal}
• MACD Trend: {macd_trend}

=== VOLATILITY & SUPPORT/RESISTANCE ===
• ATR (Volatility): {atr_value}
• Bollinger Bands: Price is {bb_position}
• BB Width: {bb_width} - Volatility is {volatility_level}
• Distance to Upper Band: {dist_to_upper}%
• Distance to Lower Band: {dist_to_lower}%

=== VOLUME ANALYSIS ===
• Current Volume vs Average: {volume_ratio}x
• Volume Trend: {volume_trend}
• OBV (On-Balance Volume): {obv_trend}
• Volume Confirmation: {volume_confirmation}

=== RISK ASSESSMENT ===
• Market Volatility: {market_volatility}
• Risk Level: {risk_level}
• Recommended Position Size: {position_size}%
• Stop Loss Level: ${stop_loss_price} (-{stop_loss_pct}%)
• Take Profit Level: ${take_profit_price} (+{take_profit_pct}%)

=== TRADE SETUP QUALITY ===
• Setup Score: {setup_score}/10
• Confluence: {confluence} indicators align
• Risk/Reward Ratio: 1:{risk_reward_ratio}

=== CRITICAL ANALYSIS ===
Based on this comprehensive multi-timeframe technical analysis, provide your trading decision.

DECISION RULES:
• BUY: Only if multiple bullish signals align (RSI not overbought, uptrend, volume confirmation, setup score ≥7)
• SELL: Only if multiple bearish signals align (RSI not oversold, downtrend, volume confirmation, setup score ≥7)
• HOLD: If signals are mixed, setup quality is low, or uncertainty is high (default to capital preservation)

IMPORTANT: Be conservative. Only suggest BUY/SELL if you have HIGH CONFIDENCE (≥80%).
When in doubt, choose HOLD to preserve capital.

Your response must be EXACTLY ONE WORD: BUY, SELL, or HOLD.
"""

def setup_log_file():
    """Creates the V2 comparison log file with enhanced header."""
    if not os.path.exists(COMPARISON_LOG_V2):
        with open(COMPARISON_LOG_V2, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Timestamp', 'Cycle', 'Symbol', 'Price', 
                'RSI', 'Stochastic', 'MACD_Signal', 'ADX', 'Trend',
                'Volume_Ratio', 'Volatility', 'Setup_Score',
                'Model_Name', 'Model_Signal', 'Model_Response_Time_ms',
                'Consensus_Signal', 'Agreement_Level', 'Confidence_Score',
                'Stop_Loss', 'Take_Profit', 'Risk_Reward_Ratio'
            ])
        print(f"[OK] Created log file: {COMPARISON_LOG_V2}")

def log_comparison_v2(log_data):
    """Appends enhanced comparison data to CSV."""
    with open(COMPARISON_LOG_V2, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            log_data.get('timestamp'),
            log_data.get('cycle'),
            log_data.get('symbol'),
            log_data.get('price'),
            log_data.get('rsi'),
            log_data.get('stochastic'),
            log_data.get('macd_signal'),
            log_data.get('adx'),
            log_data.get('trend'),
            log_data.get('volume_ratio'),
            log_data.get('volatility'),
            log_data.get('setup_score'),
            log_data.get('model_name'),
            log_data.get('model_signal'),
            log_data.get('response_time'),
            log_data.get('consensus_signal'),
            log_data.get('agreement_level'),
            log_data.get('confidence_score'),
            log_data.get('stop_loss'),
            log_data.get('take_profit'),
            log_data.get('risk_reward_ratio')
        ])

def get_binance_client():
    """Initializes Binance client."""
    try:
        client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)
        client.get_account()
        print("[OK] Connected to Binance Testnet")
        return client
    except Exception as e:
        print(f"[ERROR] Connecting to Binance: {e}")
        return None

def get_market_data(client, symbol, interval, limit=KLINES_LIMIT):
    """Fetches extended market data."""
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ])
        
        # Convert to numeric
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col])
        
        return df
    except Exception as e:
        print(f"[ERROR] Fetching market data: {e}")
        return None

def calculate_enhanced_indicators(df):
    """Calculates comprehensive technical indicators."""
    if df is None or len(df) < max(RSI_PERIOD, EMA_LONG, MACD_SLOW):
        print("[ERROR] Insufficient data for indicators")
        return None
    
    try:
        current_price = df['close'].iloc[-1]
        
        # === RSI ===
        rsi_indicator = RSIIndicator(close=df['close'], window=RSI_PERIOD)
        rsi = rsi_indicator.rsi().iloc[-1]
        
        if rsi < RSI_OVERSOLD:
            rsi_signal = "OVERSOLD - Strong Buy Signal"
        elif rsi > RSI_OVERBOUGHT:
            rsi_signal = "OVERBOUGHT - Strong Sell Signal"
        elif rsi < 40:
            rsi_signal = "Bearish Territory"
        elif rsi > 60:
            rsi_signal = "Bullish Territory"
        else:
            rsi_signal = "NEUTRAL"
        
        # === Stochastic Oscillator ===
        stoch = StochasticOscillator(high=df['high'], low=df['low'], close=df['close'], window=STOCH_PERIOD)
        stoch_k = stoch.stoch().iloc[-1]
        stoch_signal = "OVERSOLD" if stoch_k < 20 else "OVERBOUGHT" if stoch_k > 80 else "NEUTRAL"
        
        # === MACD ===
        macd_indicator = MACD(close=df['close'], window_fast=MACD_FAST, window_slow=MACD_SLOW, window_sign=MACD_SIGNAL)
        macd = macd_indicator.macd().iloc[-1]
        macd_signal_line = macd_indicator.macd_signal().iloc[-1]
        macd_hist = macd_indicator.macd_diff().iloc[-1]
        
        if macd > macd_signal_line and macd_hist > 0:
            macd_signal_text = "BULLISH - Strong Momentum"
            macd_trend = "Upward"
        elif macd < macd_signal_line and macd_hist < 0:
            macd_signal_text = "BEARISH - Downward Pressure"
            macd_trend = "Downward"
        else:
            macd_signal_text = "NEUTRAL - Consolidation"
            macd_trend = "Sideways"
        
        # === EMAs (Multiple Timeframes) ===
        ema_short_ind = EMAIndicator(close=df['close'], window=EMA_SHORT)
        ema_medium_ind = EMAIndicator(close=df['close'], window=EMA_MEDIUM)
        ema_long_ind = EMAIndicator(close=df['close'], window=EMA_LONG)
        
        ema_short = ema_short_ind.ema_indicator().iloc[-1]
        ema_medium = ema_medium_ind.ema_indicator().iloc[-1]
        ema_long = ema_long_ind.ema_indicator().iloc[-1]
        
        price_vs_ema_short = "ABOVE (+)" if current_price > ema_short else "BELOW (-)"
        price_vs_ema_medium = "ABOVE (+)" if current_price > ema_medium else "BELOW (-)"
        price_vs_ema_long = "ABOVE (+)" if current_price > ema_long else "BELOW (-)"
        
        # EMA Alignment (bullish when short > medium > long)
        if ema_short > ema_medium > ema_long:
            ema_alignment = "BULLISH - Perfect Alignment"
        elif ema_short < ema_medium < ema_long:
            ema_alignment = "BEARISH - Perfect Alignment"
        else:
            ema_alignment = "MIXED - No Clear Alignment"
        
        # === Trend Analysis ===
        short_trend = "BULLISH" if (current_price > ema_short and ema_short > ema_medium) else "BEARISH" if (current_price < ema_short and ema_short < ema_medium) else "NEUTRAL"
        medium_trend = "BULLISH" if current_price > ema_medium else "BEARISH"
        long_trend = "BULLISH" if current_price > ema_long else "BEARISH"
        
        # === ADX (Trend Strength) ===
        adx_indicator = ADXIndicator(high=df['high'], low=df['low'], close=df['close'], window=ADX_PERIOD)
        adx = adx_indicator.adx().iloc[-1]
        
        if adx > 50:
            adx_signal = "VERY STRONG Trend"
        elif adx > 25:
            adx_signal = "STRONG Trend"
        elif adx > 20:
            adx_signal = "Emerging Trend"
        else:
            adx_signal = "WEAK Trend / Ranging"
        
        # === Bollinger Bands ===
        bb_indicator = BollingerBands(close=df['close'], window=20, window_dev=2)
        bb_high = bb_indicator.bollinger_hband().iloc[-1]
        bb_low = bb_indicator.bollinger_lband().iloc[-1]
        bb_mid = bb_indicator.bollinger_mavg().iloc[-1]
        bb_width = ((bb_high - bb_low) / bb_mid) * 100
        
        dist_to_upper = ((bb_high - current_price) / current_price) * 100
        dist_to_lower = ((current_price - bb_low) / current_price) * 100
        
        if current_price > bb_high:
            bb_position = "ABOVE upper band - Overbought"
        elif current_price < bb_low:
            bb_position = "BELOW lower band - Oversold"
        elif current_price > bb_mid:
            bb_position = "Upper half - Bullish"
        else:
            bb_position = "Lower half - Bearish"
        
        volatility_level = "HIGH" if bb_width > 4 else "MEDIUM" if bb_width > 2 else "LOW"
        
        # === ATR (Average True Range - Volatility) ===
        atr_indicator = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=ATR_PERIOD)
        atr = atr_indicator.average_true_range().iloc[-1]
        atr_percent = (atr / current_price) * 100
        
        # === Volume Analysis ===
        current_volume = df['volume'].iloc[-1]
        avg_volume = df['volume'].rolling(window=20).mean().iloc[-1]
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
        
        if volume_ratio > 1.5:
            volume_trend = "SURGING - Strong Interest"
            volume_confirmation = "CONFIRMED"
        elif volume_ratio > 1.2:
            volume_trend = "INCREASING - Growing Interest"
            volume_confirmation = "CONFIRMED"
        elif volume_ratio < 0.7:
            volume_trend = "DECLINING - Weak Interest"
            volume_confirmation = "WEAK"
        else:
            volume_trend = "NORMAL"
            volume_confirmation = "NEUTRAL"
        
        # Calculate 24h volume
        volume_24h = df['volume'].tail(24).sum() * current_price if len(df) >= 24 else current_volume * current_price
        
        # === OBV (On-Balance Volume) ===
        obv_indicator = OnBalanceVolumeIndicator(close=df['close'], volume=df['volume'])
        obv = obv_indicator.on_balance_volume().iloc[-1]
        obv_prev = obv_indicator.on_balance_volume().iloc[-2]
        obv_trend = "ACCUMULATION (+)" if obv > obv_prev else "DISTRIBUTION (-)"
        
        # === Price Change Analysis ===
        if len(df) >= 24:
            price_24h_ago = df['close'].iloc[-24]
            price_change = ((current_price - price_24h_ago) / price_24h_ago) * 100
            price_avg_24h = df['close'].tail(24).mean()
            price_vs_avg = ((current_price - price_avg_24h) / price_avg_24h) * 100
        else:
            price_change = 0
            price_vs_avg = 0
        
        # === Risk Management Calculations ===
        stop_loss_price = current_price * (1 - STOP_LOSS_PERCENT)
        take_profit_price = current_price * (1 + TAKE_PROFIT_PERCENT)
        risk_reward_ratio = TAKE_PROFIT_PERCENT / STOP_LOSS_PERCENT
        
        # === Market Risk Assessment ===
        if atr_percent > 3:
            market_volatility = "VERY HIGH"
            risk_level = "HIGH RISK"
            position_size = 25
        elif atr_percent > 2:
            market_volatility = "HIGH"
            risk_level = "ELEVATED RISK"
            position_size = 50
        elif atr_percent > 1:
            market_volatility = "MODERATE"
            risk_level = "NORMAL RISK"
            position_size = 75
        else:
            market_volatility = "LOW"
            risk_level = "LOW RISK"
            position_size = 100
        
        # === Setup Quality Score (0-10) ===
        setup_score = 0
        confluence = 0
        
        # Trend alignment
        if short_trend == "BULLISH" and medium_trend == "BULLISH" and long_trend == "BULLISH":
            setup_score += 3
            confluence += 1
        elif short_trend == "BEARISH" and medium_trend == "BEARISH" and long_trend == "BEARISH":
            setup_score += 3
            confluence += 1
        
        # RSI confirmation
        if (rsi < RSI_OVERSOLD and short_trend == "BULLISH") or (rsi > RSI_OVERBOUGHT and short_trend == "BEARISH"):
            setup_score += 2
            confluence += 1
        
        # MACD confirmation
        if (macd_trend == "Upward" and short_trend == "BULLISH") or (macd_trend == "Downward" and short_trend == "BEARISH"):
            setup_score += 2
            confluence += 1
        
        # Volume confirmation
        if volume_confirmation == "CONFIRMED":
            setup_score += 2
            confluence += 1
        
        # ADX strength
        if adx > 25:
            setup_score += 1
            confluence += 1
        
        return {
            # Price
            'current_price': round(current_price, 2),
            'price_change': round(price_change, 2),
            'price_vs_avg': round(price_vs_avg, 2),
            'volume_24h': round(volume_24h, 2),
            
            # Momentum
            'rsi_value': round(rsi, 2),
            'rsi_signal': rsi_signal,
            'stoch_k': round(stoch_k, 2),
            'stoch_signal': stoch_signal,
            'macd_value': round(macd, 4),
            'macd_signal_value': round(macd_signal_line, 4),
            'macd_hist': round(macd_hist, 4),
            'macd_signal': macd_signal_text,
            'macd_trend': macd_trend,
            
            # Trend
            'ema_short': round(ema_short, 2),
            'ema_medium': round(ema_medium, 2),
            'ema_long': round(ema_long, 2),
            'price_vs_ema_short': price_vs_ema_short,
            'price_vs_ema_medium': price_vs_ema_medium,
            'price_vs_ema_long': price_vs_ema_long,
            'ema_alignment': ema_alignment,
            'short_trend': short_trend,
            'medium_trend': medium_trend,
            'long_trend': long_trend,
            'adx_value': round(adx, 2),
            'adx_signal': adx_signal,
            
            # Volatility
            'bb_position': bb_position,
            'bb_width': round(bb_width, 2),
            'volatility_level': volatility_level,
            'dist_to_upper': round(dist_to_upper, 2),
            'dist_to_lower': round(dist_to_lower, 2),
            'atr_value': round(atr, 2),
            'market_volatility': market_volatility,
            
            # Volume
            'volume_ratio': round(volume_ratio, 2),
            'volume_trend': volume_trend,
            'obv_trend': obv_trend,
            'volume_confirmation': volume_confirmation,
            
            # Risk Management
            'risk_level': risk_level,
            'position_size': position_size,
            'stop_loss_price': round(stop_loss_price, 2),
            'take_profit_price': round(take_profit_price, 2),
            'stop_loss_pct': round(STOP_LOSS_PERCENT * 100, 1),
            'take_profit_pct': round(TAKE_PROFIT_PERCENT * 100, 1),
            'risk_reward_ratio': round(risk_reward_ratio, 2),
            
            # Setup Quality
            'setup_score': setup_score,
            'confluence': confluence
        }
        
    except Exception as e:
        print(f"[ERROR] Calculating indicators: {e}")
        return None

def get_model_signal_v2(model_info, technical_data, symbol):
    """Gets trading signal from a specific model with enhanced context."""
    try:
        start_time = time.time()
        
        client = Groq()
        prompt_content = PROMPT_TEMPLATE_V2.format(symbol=symbol, **technical_data)
        
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
        print(f"[ERROR] Model {model_info['display_name']}: {e}")
        return "ERROR", 0, str(e)

def calculate_enhanced_consensus(signals, setup_score):
    """Calculates consensus with confidence scoring."""
    signal_counts = {'BUY': 0, 'SELL': 0, 'HOLD': 0, 'ERROR': 0}
    
    for signal in signals:
        if signal in signal_counts:
            signal_counts[signal] += 1
    
    # Remove errors from consensus
    valid_signals = {k: v for k, v in signal_counts.items() if k != 'ERROR'}
    
    if not valid_signals or sum(valid_signals.values()) == 0:
        return "HOLD", 0, 0
    
    consensus = max(valid_signals, key=valid_signals.get)
    total_valid = sum(valid_signals.values())
    agreement_level = (valid_signals[consensus] / total_valid) * 100
    
    # Confidence score: combination of agreement and setup quality
    confidence_score = (agreement_level * 0.7) + (setup_score * 10 * 0.3)
    
    # Override to HOLD if confidence is too low
    if confidence_score < CONFIDENCE_THRESHOLD and consensus != "HOLD":
        print(f"[RISK] Low confidence ({confidence_score:.1f}%), overriding to HOLD")
        consensus = "HOLD"
    
    return consensus, round(agreement_level, 1), round(confidence_score, 1)

def main():
    """Main V2 comparison function with enhanced features."""
    print("=" * 80)
    print("[BOT] TRADING BOT - MODEL COMPARISON V2 (OPTIMIZED)")
    print("=" * 80)
    print(f"\n[INFO] Testing {len(MODELS_V2)} NEW models:")
    for i, model in enumerate(MODELS_V2, 1):
        print(f"  {i}. {model['display_name']}: {model['description']}")
    
    print(f"\n[CONFIG] Trading Setup:")
    print(f"  Symbol: {SYMBOL}")
    print(f"  Timeframe: {timeframe_str}")
    print(f"  Stop Loss: {STOP_LOSS_PERCENT*100}%")
    print(f"  Take Profit: {TAKE_PROFIT_PERCENT*100}%")
    print(f"  Risk/Reward: 1:{TAKE_PROFIT_PERCENT/STOP_LOSS_PERCENT:.1f}")
    print(f"  Confidence Threshold: {CONFIDENCE_THRESHOLD}%")
    print(f"  Results: {COMPARISON_LOG_V2}")
    print("=" * 80)
    
    setup_log_file()
    binance_client = get_binance_client()
    if not binance_client:
        return
    
    cycle_count = 0
    
    while True:
        cycle_count += 1
        print(f"\n{'='*80}")
        print(f"[CYCLE] #{cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        # Fetch market data
        df = get_market_data(binance_client, SYMBOL, INTERVAL)
        
        if df is not None and len(df) > 0:
            technical_data = calculate_enhanced_indicators(df)
            
            if technical_data:
                current_price = technical_data['current_price']
                setup_score = technical_data['setup_score']
                
                print(f"\n[DATA] MARKET SNAPSHOT:")
                print(f"  Price: ${current_price} ({technical_data['price_change']:+.2f}%)")
                print(f"  Trend: {technical_data['short_trend']} / {technical_data['medium_trend']} / {technical_data['long_trend']}")
                print(f"  RSI: {technical_data['rsi_value']} - {technical_data['rsi_signal']}")
                print(f"  ADX: {technical_data['adx_value']} - {technical_data['adx_signal']}")
                print(f"  Volume: {technical_data['volume_ratio']:.2f}x avg - {technical_data['volume_trend']}")
                print(f"  Volatility: {technical_data['market_volatility']} - {technical_data['risk_level']}")
                print(f"  Setup Quality: {setup_score}/10 ({technical_data['confluence']} indicators)")
                
                print(f"\n[RISK] Risk Management:")
                print(f"  Stop Loss: ${technical_data['stop_loss_price']} (-{technical_data['stop_loss_pct']}%)")
                print(f"  Take Profit: ${technical_data['take_profit_price']} (+{technical_data['take_profit_pct']}%)")
                print(f"  R/R Ratio: 1:{technical_data['risk_reward_ratio']}")
                
                print(f"\n[MODELS] Querying {len(MODELS_V2)} models...")
                print(f"{'Model':<25} {'Signal':<8} {'Response Time':<15}")
                print("-" * 50)
                
                signals = []
                response_times = []
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Query all models
                for model in MODELS_V2:
                    signal, response_time, raw = get_model_signal_v2(model, technical_data, SYMBOL)
                    signals.append(signal)
                    response_times.append(response_time)
                    
                    # Display result
                    tag = "[BUY]" if signal == "BUY" else "[SELL]" if signal == "SELL" else "[HOLD]" if signal == "HOLD" else "[ERROR]"
                    print(f"{tag} {model['display_name']:<23} {signal:<8} {response_time:.0f}ms")
                
                # Calculate enhanced consensus
                consensus_signal, agreement_level, confidence_score = calculate_enhanced_consensus(signals, setup_score)
                
                print(f"\n{'='*50}")
                print(f"[CONSENSUS] {consensus_signal}")
                print(f"  Agreement: {agreement_level}%")
                print(f"  Confidence: {confidence_score:.1f}/100")
                print(f"  Status: {'TRADEABLE' if confidence_score >= CONFIDENCE_THRESHOLD else 'LOW CONFIDENCE - HOLD'}")
                print(f"{'='*50}")
                
                # Log each model's result
                for i, model in enumerate(MODELS_V2):
                    log_data = {
                        'timestamp': timestamp,
                        'cycle': cycle_count,
                        'symbol': SYMBOL,
                        'price': current_price,
                        'rsi': technical_data['rsi_value'],
                        'stochastic': technical_data['stoch_k'],
                        'macd_signal': technical_data['macd_signal'],
                        'adx': technical_data['adx_value'],
                        'trend': f"{technical_data['short_trend']}/{technical_data['medium_trend']}/{technical_data['long_trend']}",
                        'volume_ratio': technical_data['volume_ratio'],
                        'volatility': technical_data['market_volatility'],
                        'setup_score': setup_score,
                        'model_name': model['display_name'],
                        'model_signal': signals[i],
                        'response_time': response_times[i],
                        'consensus_signal': consensus_signal,
                        'agreement_level': agreement_level,
                        'confidence_score': confidence_score,
                        'stop_loss': technical_data['stop_loss_price'],
                        'take_profit': technical_data['take_profit_price'],
                        'risk_reward_ratio': technical_data['risk_reward_ratio']
                    }
                    log_comparison_v2(log_data)
                
                print(f"\n[OK] Results logged to {COMPARISON_LOG_V2}")
            else:
                print("[ERROR] Failed to calculate technical indicators")
        else:
            print("[ERROR] Failed to fetch market data")
        
        print(f"\n[WAIT] Next cycle in {WAIT_TIME//60} minutes...")
        time.sleep(WAIT_TIME)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[EXIT] Bot stopped by user")
    except Exception as e:
        print(f"\n[ERROR] Critical error: {e}")
