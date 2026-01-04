# Polymarket Market Scanner - Phase 1

Real-time monitoring system for detecting unusual trading activity on Polymarket.

## What It Does

The scanner continuously monitors Polymarket markets and alerts you when it detects:

- 🐋 **Whale Trades**: Large positions ($5000+) being taken
- 📈 **Rapid Price Movements**: Significant price changes in short timeframes
- 💰 **Large Positions**: Top holders with substantial stakes
- 🎯 **Contrarian Bets**: Big money on low-probability outcomes (potential insider activity)
- 📊 **Volume Spikes**: Unusual trading volume compared to historical average
- 🎪 **Market Concentration**: Single wallets controlling large portions of markets

## Documentation (Choose Your Path)

**👋 New to this? Not technical?**
→ Start here: **[QUICK_START.md](QUICK_START.md)** (5 minutes)
→ Then read: **[SOP_BEGINNERS.md](SOP_BEGINNERS.md)** (Complete guide)
→ Print this: **[DAILY_CHECKLIST.md](DAILY_CHECKLIST.md)** (Daily workflow)

**💻 Technical user?**
→ Read: **[SETUP_GUIDE.md](SETUP_GUIDE.md)** (Installation details)
→ Reference: **[SOP.md](SOP.md)** (Advanced operations)

**🎯 Just want to see it work?**
→ **[QUICK_START.md](QUICK_START.md)** (Copy/paste 4 commands, done)

## Absolute Quickest Start

```bash
cd /home/user/me/polymarket_scanner
pip3 install -r requirements.txt
python3 scanner.py
```

Press `Ctrl+C` to stop. That's it!

## Configuration

Edit `config.py` to customize:

- **Scan interval**: How often to check markets
- **Thresholds**: What counts as "large" trade, whale activity, etc.
- **Alert levels**: Which types of alerts to show
- **Tracking**: Auto-track wallets that make large trades

### Key Thresholds

```python
LARGE_TRADE_MIN_USD = 1000      # Trades over $1000
WHALE_TRADE_MIN_USD = 5000      # Trades over $5000
LARGE_POSITION_MIN_USD = 2000   # Positions over $2000
WHALE_POSITION_MIN_USD = 10000  # Positions over $10000

LOW_PROBABILITY_THRESHOLD = 0.15   # Alert on large bets <15¢
HIGH_PROBABILITY_THRESHOLD = 0.85  # Alert on large bets >85¢
```

## Example Output

```
🔍 Polymarket Scanner initialized
   Scan interval: 60s
   Large trade threshold: $1000
   Whale trade threshold: $5000

🔄 Starting scan at 14:23:15
   Scanning 47 markets...

🚨 CRITICAL: Will Bitcoin reach $100k by end of year?
   🐋 WHALE trade: $7,500 BUY at LOW price 0.073 - POTENTIAL INSIDER?
   • wallet: 0x1234567...
   • trade_value: $7,500
   • price: 0.073

⚠️  WARNING: US Presidential Election 2024
   High concentration: Top holder owns 34.2% of YES
   • concentration: 34.2%
   • wallet: 0xabcdef1...

   ⚡ Scan complete - 2 alerts generated
   Tracked wallets: 3
```

## Data Persistence

All activity is logged to `data/` directory:

- **alerts.jsonl**: All alerts in JSON Lines format
- **whale_wallets.json**: Auto-discovered whale wallets
- **market_snapshots.jsonl**: Historical market data (for future phases)

## What's Next

This is **Phase 1**. Future phases will add:

- **Phase 2**: Whale wallet tracking and historical performance analysis
- **Phase 3**: Real-time monitoring of proven "smart money" wallets
- **Phase 4**: Web dashboard and advanced analytics

## API Usage

The scanner uses Polymarket's public APIs:
- **Gamma API**: Market metadata and discovery
- **Data API**: Trades, positions, holders
- **CLOB API**: Order book and pricing

No authentication required for read-only access.

## Tips

1. **Start conservative**: Run with default thresholds first
2. **Adjust thresholds**: Tune based on what you consider "unusual"
3. **Monitor alerts.jsonl**: Review historical alerts to improve detection
4. **Track good wallets**: Add proven traders to `MANUALLY_TRACKED_WALLETS`

## Example: Venezuela President Case

If someone bought a large YES position at 7¢:

```
🚨 CRITICAL: Will Venezuela president resign?
   🐋 WHALE trade: $5,000 BUY at LOW price 0.070 - POTENTIAL INSIDER?
   • wallet: 0x9876543...
   • trade_value: $5,000
   • price: 0.070
```

The scanner would:
1. Alert you immediately
2. Log the wallet address
3. Auto-track that wallet for future trades
4. Save alert details to data/alerts.jsonl

## License

MIT
