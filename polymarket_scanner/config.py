"""
Configuration for Polymarket Scanner
Adjust these thresholds based on what you consider "unusual activity"
"""

# ==================== SCANNING SETTINGS ====================

# How often to scan markets (seconds)
SCAN_INTERVAL = 60

# Number of markets to monitor per scan
MAX_MARKETS_TO_SCAN = 100

# Only scan markets with minimum volume (USD)
MIN_MARKET_VOLUME = 5000

# ==================== ANOMALY DETECTION THRESHOLDS ====================

# Large Trade Detection
LARGE_TRADE_MIN_USD = 1000  # Trades over $1000 are considered "large"
WHALE_TRADE_MIN_USD = 5000  # Trades over $5000 are "whale" activity

# Price Movement Detection
RAPID_PRICE_CHANGE_PERCENT = 10  # Alert if price moves >10% in scan interval
EXTREME_PRICE_CHANGE_PERCENT = 25  # Alert if price moves >25%

# Position Size Detection
LARGE_POSITION_MIN_USD = 2000  # Positions over $2000 in a single outcome
WHALE_POSITION_MIN_USD = 10000  # Positions over $10000

# Volume Spike Detection
VOLUME_SPIKE_MULTIPLIER = 3.0  # Alert if volume is 3x recent average

# Market Oddities
LOW_PROBABILITY_THRESHOLD = 0.15  # Alert on large bets when price <15¢
HIGH_PROBABILITY_THRESHOLD = 0.85  # Alert on large bets when price >85¢

# Concentration Detection
TOP_HOLDER_CONCENTRATION = 0.30  # Alert if top holder has >30% of market

# ==================== ALERT SETTINGS ====================

# Alert levels
ALERT_INFO = "INFO"      # Interesting but not urgent
ALERT_WARNING = "WARNING"  # Unusual activity worth noting
ALERT_CRITICAL = "CRITICAL"  # Major whale activity or extreme moves

# Console output settings
COLORIZE_OUTPUT = True
SHOW_INFO_ALERTS = True
SHOW_WARNING_ALERTS = True
SHOW_CRITICAL_ALERTS = True

# ==================== DATA PERSISTENCE ====================

# Where to store historical data
DATA_DIR = "data"
ALERTS_LOG_FILE = f"{DATA_DIR}/alerts.jsonl"
MARKET_SNAPSHOTS_FILE = f"{DATA_DIR}/market_snapshots.jsonl"
WHALE_WALLETS_FILE = f"{DATA_DIR}/whale_wallets.json"

# How long to keep historical data for comparison (seconds)
PRICE_HISTORY_WINDOW = 3600  # 1 hour
VOLUME_HISTORY_WINDOW = 7200  # 2 hours

# ==================== RATE LIMITING ====================

# API request delays (seconds)
API_REQUEST_DELAY = 0.1  # Small delay between requests to be respectful

# ==================== WALLET TRACKING ====================

# Automatically track wallets that make trades above this threshold
AUTO_TRACK_WALLET_MIN_TRADE = 5000

# Maximum number of wallets to auto-track
MAX_AUTO_TRACKED_WALLETS = 50

# Manually tracked wallets (add addresses here as you find good traders)
MANUALLY_TRACKED_WALLETS = [
    # Add wallet addresses you want to monitor
    # Example: "0x1234567890abcdef1234567890abcdef12345678"
]
