# Example Scanner Output

This shows what the scanner will display when running and detecting unusual activity.

## Startup

```
🔍 Polymarket Scanner initialized
   Scan interval: 60s
   Large trade threshold: $1000
   Whale trade threshold: $5000

============================================================
  POLYMARKET SCANNER - PHASE 1
  Monitoring for unusual market activity...
============================================================
```

## Normal Scan (No Alerts)

```
🔄 Starting scan at 14:23:15
   Scanning 47 markets...
   ✓ Scan complete - no unusual activity detected
   Tracked wallets: 0

   💤 Waiting 60s until next scan...
   --------------------------------------------------
```

## Scan with Whale Activity Detected

```
🔄 Starting scan at 14:24:15
   Scanning 47 markets...

🚨 CRITICAL: Will Venezuela president step down in 2026?
   🐋 WHALE trade: $7,500 BUY at LOW price 0.073 - POTENTIAL INSIDER?
   • wallet: 0x742d35C...
   • trade_value: $7,500
   • side: BUY
   • price: 0.073
   • size: 102,740

⚠️  WARNING: Bitcoin above $100k by end of 2026?
   Rapid price movement on YES: +12.3%
   • outcome: YES
   • current_price: 0.423
   • change: +12.3%

🚨 CRITICAL: US Presidential Election 2028
   🐋 WHALE position detected: #1 holder has $15,000 in YES
   • wallet: 0x9a8f123...
   • position_value: $15,000
   • outcome: YES
   • rank: #1

⚠️  WARNING: US Presidential Election 2028
   High concentration: Top holder owns 34.2% of YES
   • concentration: 34.2%
   • wallet: 0x9a8f123...

ℹ️  INFO: Ethereum above $5000 in 2026?
   Volume spike detected: 3.2x normal
   • current_volume: $45,670
   • spike_ratio: 3.2x

   ⚡ Scan complete - 5 alerts generated
   Tracked wallets: 2

   💤 Waiting 60s until next scan...
   --------------------------------------------------
```

## What Each Alert Means

### 🚨 CRITICAL Alerts

**Whale Trade with Low Probability**
- Someone bet $7,500 on 7.3% odds
- This is unusual - either they have information or are making a huge mistake
- Wallet is automatically tracked for future trades

**Whale Position**
- Top holder has $15,000 in a single outcome
- Shows serious conviction or insider knowledge
- Wallet is tracked

### ⚠️ WARNING Alerts

**Rapid Price Movement**
- Price moved >10% in the scan window (60 seconds)
- Could indicate:
  - News breaking
  - Large order executed
  - Market sentiment shift

**High Concentration**
- Single wallet controls >30% of outcome
- Market is susceptible to manipulation
- Price may be unreliable

**Volume Spike**
- Trading volume is 3x normal
- Increased activity suggests:
  - New information
  - Viral attention
  - Potential opportunity

### ℹ️ INFO Alerts

**General unusual patterns**
- Lower priority observations
- May be noise or early signals

## Log Files

All alerts are saved to `data/alerts.jsonl`:

```json
{"timestamp": "2026-01-04T14:24:15", "level": "CRITICAL", "market": "Will Venezuela president step down in 2026?", "message": "🐋 WHALE trade: $7,500 BUY at LOW price 0.073 - POTENTIAL INSIDER?", "data": {"wallet": "0x742d35C...", "trade_value": "$7,500", "side": "BUY", "price": "0.073", "size": "102,740"}}
```

Discovered whale wallets saved to `data/whale_wallets.json`:

```json
[
  {
    "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEaE",
    "discovered_at": "2026-01-04T14:24:15",
    "discovery_trade_value": 7500.0
  }
]
```

## Next Steps

1. **Monitor the alerts** - See what patterns emerge
2. **Tune thresholds** - Adjust `config.py` based on what you see
3. **Track wallets** - Add successful wallets to manual tracking
4. **Analyze logs** - Review `data/alerts.jsonl` for patterns
5. **Phase 2** - Build wallet performance tracker
