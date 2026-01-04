# Polymarket Scanner - Complete Setup Guide

## Prerequisites

- Python 3.9 or higher
- Internet connection (for API access)
- Terminal/command line access

## Installation Steps

### 1. Install Dependencies

```bash
cd polymarket_scanner
pip install -r requirements.txt
```

This installs:
- `requests` - HTTP library for API calls
- `py-clob-client` - Official Polymarket CLOB client

### 2. Configure Settings (Optional)

The scanner works out of the box with sensible defaults. To customize:

```bash
# Edit config.py in your favorite editor
nano config.py   # or vim, code, etc.
```

Key settings to consider:
- `SCAN_INTERVAL`: How often to check (default 60s)
- `LARGE_TRADE_MIN_USD`: What you consider a "large" trade (default $1000)
- `WHALE_TRADE_MIN_USD`: Whale threshold (default $5000)
- `MIN_MARKET_VOLUME`: Ignore low-volume markets (default $5000)

### 3. Run the Scanner

```bash
python scanner.py
```

The scanner will:
- Connect to Polymarket APIs
- Start monitoring active markets
- Display alerts in real-time
- Log all activity to `data/` directory

### 4. Stop the Scanner

Press `Ctrl+C` to stop gracefully.

The scanner will show a summary:
```
🛑 Scanner stopped by user
   Total whale wallets discovered: 3
   Alerts saved to: data/alerts.jsonl
```

## Understanding the Output

### Alert Levels

**🚨 CRITICAL (Red)**
- Whale trades (>$5000)
- Extreme price movements (>25%)
- Potential insider activity (large bets on low-probability outcomes)

**⚠️ WARNING (Yellow)**
- Large trades (>$1000)
- Rapid price changes (>10%)
- High market concentration
- Volume spikes

**ℹ️ INFO (Cyan)**
- General observations
- Interesting patterns

### Reading a Whale Alert

```
🚨 CRITICAL: Will Bitcoin reach $100k by end of year?
   🐋 WHALE trade: $7,500 BUY at LOW price 0.073 - POTENTIAL INSIDER?
   • wallet: 0x742d35C...
   • trade_value: $7,500
   • side: BUY
   • price: 0.073
   • size: 102,740
```

This means:
- Market: Bitcoin $100k prediction
- Someone bought $7,500 worth of YES
- Current price is only 7.3¢ (7.3% probability)
- This is highly contrarian - possible insider information
- Their wallet is now being tracked

## Data Files

All data is saved to the `data/` directory:

### alerts.jsonl
Every alert in JSON format (one per line):
```json
{"timestamp": "2026-01-04T14:24:15", "level": "CRITICAL", ...}
```

You can analyze this later:
```bash
# Count alerts by level
grep "CRITICAL" data/alerts.jsonl | wc -l

# View all whale trades
grep "WHALE trade" data/alerts.jsonl
```

### whale_wallets.json
Automatically discovered high-value traders:
```json
[
  {
    "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEaE",
    "discovered_at": "2026-01-04T14:24:15",
    "discovery_trade_value": 7500.0
  }
]
```

Use this to:
- Manually review successful traders
- Add to `MANUALLY_TRACKED_WALLETS` in config
- Build Phase 2 wallet tracker

## Common Issues

### "API Request failed"
- Check internet connection
- Polymarket APIs may be down (rare)
- Rate limiting (reduce `SCAN_INTERVAL`)

### "No markets returned"
- APIs might be temporarily unavailable
- Try again in a few minutes

### Too many/few alerts
Adjust thresholds in `config.py`:
```python
# More conservative (fewer alerts)
LARGE_TRADE_MIN_USD = 5000
WHALE_TRADE_MIN_USD = 10000

# More sensitive (more alerts)
LARGE_TRADE_MIN_USD = 500
WHALE_TRADE_MIN_USD = 2000
```

### Scanner is slow
- Reduce `MAX_MARKETS_TO_SCAN` (default 100)
- Increase `MIN_MARKET_VOLUME` to focus on liquid markets
- Increase `SCAN_INTERVAL` to scan less frequently

## Optimization Tips

### 1. Focus on High-Value Markets
```python
MIN_MARKET_VOLUME = 25000  # Only scan markets with >$25k volume
```

### 2. Only Track Critical Alerts
```python
SHOW_INFO_ALERTS = False
SHOW_WARNING_ALERTS = False
SHOW_CRITICAL_ALERTS = True
```

### 3. Faster Scanning
```python
MAX_MARKETS_TO_SCAN = 50  # Scan fewer markets
API_REQUEST_DELAY = 0.05  # Faster API calls (be respectful!)
```

## Next Steps

### Phase 1 (Current)
✅ Real-time market scanning
✅ Anomaly detection
✅ Whale discovery
✅ Alert logging

### Phase 2 (Next)
- [ ] Track whale wallet performance
- [ ] Calculate historical win rates
- [ ] Identify consistently successful traders
- [ ] Build "smart money" leaderboard

### Phase 3 (Future)
- [ ] Real-time monitoring of proven wallets
- [ ] Instant alerts when smart money moves
- [ ] Position size analysis
- [ ] Behavioral patterns

### Phase 4 (Advanced)
- [ ] Web dashboard
- [ ] Discord/Telegram notifications
- [ ] Advanced analytics
- [ ] Strategy backtesting

## Getting Help

1. Check `example_output.md` for sample alerts
2. Review `README.md` for feature overview
3. Examine `config.py` for all settings
4. Check log files in `data/` for debugging

## Tips for Success

1. **Run continuously** - The scanner is designed to run 24/7
2. **Review logs daily** - Look for patterns in `alerts.jsonl`
3. **Track good wallets** - When you see successful traders, add them manually
4. **Adjust thresholds** - Tune based on your risk tolerance
5. **Be patient** - Big opportunities are rare, but the scanner won't miss them

## Example Workflow

**Day 1:**
- Start scanner with default settings
- Observe what alerts appear
- Take notes on interesting patterns

**Day 2-3:**
- Adjust thresholds based on what you learned
- Add any consistently successful wallets to manual tracking
- Review historical alerts

**Day 4+:**
- Scanner runs with tuned settings
- You get high-quality alerts
- Start building Phase 2 (wallet tracker)

## Safety Notes

⚠️ **This is a monitoring tool, not trading advice**
- Whale activity doesn't guarantee outcomes
- Markets can be manipulated
- Always do your own research
- Never risk more than you can afford to lose

## Questions?

Review the code:
- `polymarket_api.py` - API client implementation
- `scanner.py` - Main scanning logic
- `config.py` - All configurable settings
