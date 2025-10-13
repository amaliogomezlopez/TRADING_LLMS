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
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands

# Load environment variables from .env file
load_dotenv()

# --- Load Configuration from YAML ---
def load_config(config_file='config.yml'):
    """Loads configuration from YAML file."""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print(f"✓ Configuration loaded from {config_file}")
        return config
    except FileNotFoundError:
        print(f"⚠️ Configuration file {config_file} not found. Using default values.")
        return None
    except Exception as e:
        print(f"⚠️ Error loading configuration: {e}. Using default values.")
        return None

# Load config
config = load_config()

# --- Binance Configuration ---
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# --- Trading Bot Parameters (from config or defaults) ---
if config:
    SYMBOL = config['trading']['symbol']
    QUANTITY = config['trading']['quantity']
    
    # Map timeframe string to Binance constant
    timeframe_map = {
        '1m': Client.KLINE_INTERVAL_1MINUTE,
        '5m': Client.KLINE_INTERVAL_5MINUTE,
        '15m': Client.KLINE_INTERVAL_15MINUTE,
        '1h': Client.KLINE_INTERVAL_1HOUR,
        '4h': Client.KLINE_INTERVAL_4HOUR,
        '1d': Client.KLINE_INTERVAL_1DAY
    }
    
    timeframe_str = config['trading']['timeframe']
    INTERVAL = timeframe_map.get(timeframe_str, Client.KLINE_INTERVAL_5MINUTE)
    
    # Calculate wait_time based on timeframe
    wait_time_map = {
        '1m': 60,       # 1 minute
        '5m': 300,      # 5 minutes
        '15m': 900,     # 15 minutes
        '1h': 3600,     # 1 hour
        '4h': 14400,    # 4 hours
        '1d': 86400     # 1 day
    }
    WAIT_TIME = wait_time_map.get(timeframe_str, 300)
    
    LOG_FILE = config['logging']['log_file']
    
    # Risk Management
    STOP_LOSS_PERCENT = config['risk_management']['stop_loss_percent']
    TAKE_PROFIT_PERCENT = config['risk_management']['take_profit_percent']
    MAX_TOTAL_LOSS = config['risk_management']['max_total_loss']
    
    # Technical Indicators
    RSI_PERIOD = config['technical_indicators']['rsi']['period']
    RSI_OVERSOLD = config['technical_indicators']['rsi']['oversold']
    RSI_OVERBOUGHT = config['technical_indicators']['rsi']['overbought']
    EMA_SHORT = config['technical_indicators']['ema']['short_period']
    EMA_LONG = config['technical_indicators']['ema']['long_period']
    KLINES_LIMIT = config['technical_indicators']['klines_limit']
    
    # LLM Configuration
    LLM_MODEL = config['llm']['model']
    LLM_TEMPERATURE = config['llm']['temperature']
    LLM_MAX_TOKENS = config['llm']['max_tokens']
else:
    # Default values if config file is not found
    SYMBOL = 'BTCUSDT'
    QUANTITY = 0.001
    INTERVAL = Client.KLINE_INTERVAL_5MINUTE
    WAIT_TIME = 300
    LOG_FILE = 'trading_log.csv'
    STOP_LOSS_PERCENT = 0.02
    TAKE_PROFIT_PERCENT = 0.03
    MAX_TOTAL_LOSS = -100.0
    RSI_PERIOD = 14
    RSI_OVERSOLD = 30
    RSI_OVERBOUGHT = 70
    EMA_SHORT = 9
    EMA_LONG = 21
    KLINES_LIMIT = 100
    LLM_MODEL = 'llama-3.1-8b-instant'
    LLM_TEMPERATURE = 0.3
    LLM_MAX_TOKENS = 20

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

RECENT PRICE ACTION (Last 5 candles):
{recent_candles}

Based on this comprehensive technical analysis, provide ONE of these exact words as your trading decision:
BUY - if indicators strongly suggest an upward movement
SELL - if indicators strongly suggest a downward movement  
HOLD - if signals are mixed or unclear

Your response must be ONLY one word: BUY, SELL, or HOLD.
"""

def setup_log_file():
    """Creates the log file with a header if it doesn't exist."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Symbol', 'LLM_Signal', 'Action_Taken', 'Price', 'Quantity', 
                           'Trade_PNL', 'Total_PNL', 'RSI', 'MACD', 'EMA_Signal', 'Stop_Loss', 'Take_Profit', 'LLM_Raw_Response'])

def log_to_csv(log_data):
    """Appends a new row to the CSV log file."""
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            log_data.get('timestamp'),
            log_data.get('symbol'),
            log_data.get('llm_signal'),
            log_data.get('action'),
            log_data.get('price', ''),
            log_data.get('quantity', ''),
            log_data.get('trade_pnl', ''),
            log_data.get('total_pnl', ''),
            log_data.get('rsi', ''),
            log_data.get('macd', ''),
            log_data.get('ema_signal', ''),
            log_data.get('stop_loss', ''),
            log_data.get('take_profit', ''),
            log_data.get('raw_response')
        ])

def get_binance_client():
    """Initializes and returns the Binance API client for the Testnet."""
    try:
        client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)
        client.get_account()
        print("Successfully connected to Binance Testnet.")
        return client
    except Exception as e:
        print(f"Error connecting to Binance: {e}")
        return None

def get_market_data(client, symbol, interval, limit=KLINES_LIMIT):
    """Fetches market data and returns a DataFrame with OHLCV data."""
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ])
        
        # Convert to appropriate data types
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
    """Calculates technical indicators and returns analysis dictionary."""
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
        bb_mid = bb_indicator.bollinger_mavg().iloc[-1]
        
        current_price = df['close'].iloc[-1]
        
        # Determine RSI signal
        if rsi < RSI_OVERSOLD:
            rsi_signal = "OVERSOLD (Bullish)"
        elif rsi > RSI_OVERBOUGHT:
            rsi_signal = "OVERBOUGHT (Bearish)"
        else:
            rsi_signal = "NEUTRAL"
        
        # Determine MACD signal
        if macd > macd_signal and macd_hist > 0:
            macd_signal_text = "BULLISH (Above signal line)"
        elif macd < macd_signal and macd_hist < 0:
            macd_signal_text = "BEARISH (Below signal line)"
        else:
            macd_signal_text = "NEUTRAL"
        
        # Price vs EMAs
        price_vs_ema_short = "ABOVE" if current_price > ema_short else "BELOW"
        price_vs_ema_long = "ABOVE" if current_price > ema_long else "BELOW"
        
        # Bollinger position
        if current_price > bb_high:
            bb_position = "above upper band (overbought)"
        elif current_price < bb_low:
            bb_position = "below lower band (oversold)"
        else:
            bb_position = "within bands (normal)"
        
        # Trend analysis
        if ema_short > ema_long and current_price > ema_short:
            short_trend = "BULLISH"
        elif ema_short < ema_long and current_price < ema_short:
            short_trend = "BEARISH"
        else:
            short_trend = "NEUTRAL"
        
        if current_price > ema_long:
            medium_trend = "BULLISH"
        else:
            medium_trend = "BEARISH"
        
        # Recent candles
        recent_df = df.tail(5)
        recent_candles = "\n".join([
            f"Open: {row['open']:.2f}, High: {row['high']:.2f}, Low: {row['low']:.2f}, Close: {row['close']:.2f}"
            for _, row in recent_df.iterrows()
        ])
        
        # Calculate 24h price change
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
            'recent_candles': recent_candles,
            'price_change': round(price_change, 2)
        }
        
    except Exception as e:
        print(f"Error calculating technical indicators: {e}")
        return None

def get_trading_signal_with_groq(technical_data, symbol):
    """Uses Groq API to get a signal based on technical analysis. Returns processed signal and raw response."""
    if not technical_data:
        return "HOLD", "No technical data", {}

    try:
        client = Groq()
        prompt_content = PROMPT_TEMPLATE.format(symbol=symbol, **technical_data)
        completion = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt_content}],
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
            stream=False
        )
        raw_response = completion.choices[0].message.content
        match = re.search(r'\b(BUY|SELL|HOLD)\b', raw_response.upper())
        
        if match:
            signal = match.group(1)
            # Return signal with technical data for logging
            return signal, raw_response, technical_data
        else:
            print(f"Valid signal not found in Groq's response. Raw: '{raw_response}'")
            return "HOLD", raw_response, technical_data
            
    except Exception as e:
        print(f"Error getting trading signal from Groq: {e}")
        return "HOLD", str(e), technical_data

def execute_trade(client, symbol, signal, quantity):
    """Executes a market order on the Binance Testnet."""
    order_side = Client.SIDE_BUY if signal == "BUY" else Client.SIDE_SELL
    try:
        print(f"Executing {signal} order for {quantity} {symbol}...")
        client.create_test_order(
            symbol=symbol, side=order_side, type=Client.ORDER_TYPE_MARKET, quantity=quantity
        )
        print("Test order executed successfully.")
        # Get current price to record the entry/exit price accurately
        current_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        return current_price
    except BinanceAPIException as e:
        print(f"Error executing test order: {e}")
        return None

def check_risk_management(current_price, entry_price, in_position):
    """Checks if stop-loss or take-profit should be triggered."""
    if not in_position:
        return None, None, None
    
    stop_loss_price = entry_price * (1 - STOP_LOSS_PERCENT)
    take_profit_price = entry_price * (1 + TAKE_PROFIT_PERCENT)
    
    if current_price <= stop_loss_price:
        return "STOP_LOSS", stop_loss_price, take_profit_price
    elif current_price >= take_profit_price:
        return "TAKE_PROFIT", stop_loss_price, take_profit_price
    
    return None, stop_loss_price, take_profit_price

def main():
    """Main function to run the trading bot with enhanced technical analysis and risk management."""
    print("=" * 60)
    print("ADVANCED TRADING BOT WITH TECHNICAL ANALYSIS")
    print("=" * 60)
    if config:
        timeframe_display = config['trading']['timeframe']
        print(f"📝 Configuration: Loaded from config.yml")
    else:
        timeframe_display = "5m (default)"
        print(f"📝 Configuration: Using defaults")
    print(f"Symbol: {SYMBOL}")
    print(f"Timeframe: {timeframe_display}")
    print(f"Stop Loss: {STOP_LOSS_PERCENT*100}%")
    print(f"Take Profit: {TAKE_PROFIT_PERCENT*100}%")
    print(f"Max Total Loss: ${MAX_TOTAL_LOSS}")
    print(f"LLM Model: {LLM_MODEL}")
    print("=" * 60)
    
    setup_log_file()
    binance_client = get_binance_client()
    if not binance_client:
        return

    # --- State Variables ---
    in_position = False
    entry_price = 0.0
    total_pnl = 0.0
    cycle_count = 0

    while True:
        cycle_count += 1
        print(f"\n{'='*60}")
        print(f"CYCLE #{cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Check if we've exceeded max loss
        if total_pnl <= MAX_TOTAL_LOSS:
            print(f"⚠️ CRITICAL: Maximum loss limit reached (${total_pnl:.2f})")
            print("Bot stopped to prevent further losses.")
            break
        
        # Fetch market data
        df = get_market_data(binance_client, SYMBOL, INTERVAL)
        
        if df is not None and len(df) > 0:
            print(f"✓ Market data fetched: {len(df)} candles")
            
            # Calculate technical indicators
            technical_data = calculate_technical_indicators(df)
            
            if technical_data:
                current_price = technical_data['current_price']
                print(f"\n📊 TECHNICAL ANALYSIS:")
                print(f"   Price: ${current_price} ({technical_data['price_change']:+.2f}%)")
                print(f"   RSI: {technical_data['rsi']} - {technical_data['rsi_signal']}")
                print(f"   MACD: {technical_data['macd_signal']}")
                print(f"   Trend: {technical_data['short_trend']} (short) / {technical_data['medium_trend']} (medium)")
                print(f"   EMA: Price is {technical_data['price_vs_ema_short']} EMA9, {technical_data['price_vs_ema_long']} EMA21")
                
                # Check risk management first if in position
                risk_action, stop_loss, take_profit = check_risk_management(current_price, entry_price, in_position)
                
                if risk_action:
                    print(f"\n⚠️ RISK MANAGEMENT TRIGGERED: {risk_action}")
                    price = execute_trade(binance_client, SYMBOL, 'SELL', QUANTITY)
                    if price:
                        exit_price = price
                        trade_pnl = (exit_price - entry_price) * QUANTITY
                        total_pnl += trade_pnl
                        
                        print(f"✓ Position closed at ${exit_price}")
                        print(f"   Entry: ${entry_price:.2f} → Exit: ${exit_price:.2f}")
                        print(f"   Trade P&L: ${trade_pnl:.2f}")
                        print(f"   Total P&L: ${total_pnl:.2f}")
                        
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        log_data = {
                            'timestamp': timestamp,
                            'symbol': SYMBOL,
                            'llm_signal': risk_action,
                            'action': f'SELL ({risk_action})',
                            'price': exit_price,
                            'quantity': QUANTITY,
                            'trade_pnl': round(trade_pnl, 2),
                            'total_pnl': round(total_pnl, 2),
                            'rsi': technical_data['rsi'],
                            'macd': technical_data['macd_signal'],
                            'ema_signal': f"{technical_data['short_trend']}/{technical_data['medium_trend']}",
                            'stop_loss': round(stop_loss, 2),
                            'take_profit': round(take_profit, 2),
                            'raw_response': risk_action
                        }
                        log_to_csv(log_data)
                        
                        in_position = False
                        entry_price = 0.0
                else:
                    # Get LLM signal
                    llm_signal, raw_response, tech_data = get_trading_signal_with_groq(technical_data, SYMBOL)
                    print(f"\n🤖 LLM DECISION: {llm_signal}")
                    
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    log_data = {
                        'timestamp': timestamp,
                        'symbol': SYMBOL,
                        'llm_signal': llm_signal,
                        'raw_response': raw_response.strip(),
                        'total_pnl': round(total_pnl, 2),
                        'rsi': technical_data['rsi'],
                        'macd': technical_data['macd_signal'],
                        'ema_signal': f"{technical_data['short_trend']}/{technical_data['medium_trend']}"
                    }

                    # --- ENHANCED TRADING LOGIC ---
                    if llm_signal == 'BUY' and not in_position:
                        # Additional validation: Only buy if trend is favorable
                        if technical_data['short_trend'] == 'BULLISH' or technical_data['rsi'] < RSI_OVERSOLD:
                            price = execute_trade(binance_client, SYMBOL, 'BUY', QUANTITY)
                            if price:
                                in_position = True
                                entry_price = price
                                stop_loss = entry_price * (1 - STOP_LOSS_PERCENT)
                                take_profit = entry_price * (1 + TAKE_PROFIT_PERCENT)
                                
                                print(f"✅ BUY EXECUTED at ${entry_price:.2f}")
                                print(f"   Stop Loss: ${stop_loss:.2f}")
                                print(f"   Take Profit: ${take_profit:.2f}")
                                
                                log_data.update({
                                    'action': 'BUY',
                                    'price': entry_price,
                                    'quantity': QUANTITY,
                                    'stop_loss': round(stop_loss, 2),
                                    'take_profit': round(take_profit, 2)
                                })
                        else:
                            print(f"⚠️ BUY signal ignored - unfavorable trend conditions")
                            log_data.update({'action': 'HOLD (Unfavorable conditions)'})
                    
                    elif llm_signal == 'SELL' and in_position:
                        price = execute_trade(binance_client, SYMBOL, 'SELL', QUANTITY)
                        if price:
                            exit_price = price
                            trade_pnl = (exit_price - entry_price) * QUANTITY
                            total_pnl += trade_pnl
                            
                            print(f"✅ SELL EXECUTED at ${exit_price:.2f}")
                            print(f"   Entry: ${entry_price:.2f} → Exit: ${exit_price:.2f}")
                            print(f"   Trade P&L: ${trade_pnl:.2f}")
                            print(f"   Total P&L: ${total_pnl:.2f}")
                            
                            log_data.update({
                                'action': 'SELL',
                                'price': exit_price,
                                'quantity': QUANTITY,
                                'trade_pnl': round(trade_pnl, 2),
                                'total_pnl': round(total_pnl, 2)
                            })
                            
                            in_position = False
                            entry_price = 0.0
                    
                    else:
                        # Determine hold reason
                        if llm_signal == 'BUY' and in_position:
                            action = 'HOLD (Already in position)'
                        elif llm_signal == 'SELL' and not in_position:
                            action = 'HOLD (Not in position)'
                        else:
                            action = 'HOLD'
                        
                        print(f"⏸️ {action}")
                        
                        # If in position, show current P&L
                        if in_position:
                            unrealized_pnl = (current_price - entry_price) * QUANTITY
                            print(f"   Unrealized P&L: ${unrealized_pnl:.2f}")
                            print(f"   Stop Loss: ${entry_price * (1 - STOP_LOSS_PERCENT):.2f}")
                            print(f"   Take Profit: ${entry_price * (1 + TAKE_PROFIT_PERCENT):.2f}")
                        
                        log_data.update({'action': action})

                    log_to_csv(log_data)
            else:
                print("⚠️ Failed to calculate technical indicators")
        else:
            print("⚠️ Failed to fetch market data")
        
        # Wait for next cycle - synchronized with interval
        if WAIT_TIME >= 60:
            print(f"\n⏳ Waiting {WAIT_TIME//60} minutes for next cycle...")
        else:
            print(f"\n⏳ Waiting {WAIT_TIME} seconds for next cycle...")
        time.sleep(WAIT_TIME)

if __name__ == "__main__":
    main()