"""
Polymarket Market Scanner - Phase 1
Detects unusual activity across all markets in real-time
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import os

from polymarket_api import PolymarketAPI
import config


class MarketScanner:
    """Scans Polymarket for unusual trading activity and whale movements"""

    def __init__(self):
        self.api = PolymarketAPI()
        self.price_history = defaultdict(list)  # {token_id: [(timestamp, price), ...]}
        self.volume_history = defaultdict(list)
        self.last_scan_time = {}  # {market_id: timestamp}
        self.whale_wallets = set(config.MANUALLY_TRACKED_WALLETS)

        # Ensure data directory exists
        os.makedirs(config.DATA_DIR, exist_ok=True)

        print("🔍 Polymarket Scanner initialized")
        print(f"   Scan interval: {config.SCAN_INTERVAL}s")
        print(f"   Large trade threshold: ${config.LARGE_TRADE_MIN_USD}")
        print(f"   Whale trade threshold: ${config.WHALE_TRADE_MIN_USD}")
        print()

    def colorize(self, text: str, color: str) -> str:
        """Add terminal colors to text"""
        if not config.COLORIZE_OUTPUT:
            return text

        colors = {
            'red': '\033[91m',
            'yellow': '\033[93m',
            'green': '\033[92m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
        return f"{colors.get(color, '')}{text}{colors['end']}"

    def log_alert(self, level: str, market_name: str, message: str, data: Dict = None):
        """Log an alert with timestamp and metadata"""
        timestamp = datetime.now().isoformat()

        alert = {
            'timestamp': timestamp,
            'level': level,
            'market': market_name,
            'message': message,
            'data': data or {}
        }

        # Write to log file
        with open(config.ALERTS_LOG_FILE, 'a') as f:
            f.write(json.dumps(alert) + '\n')

        # Console output with color coding
        if level == config.ALERT_CRITICAL and config.SHOW_CRITICAL_ALERTS:
            color = 'red'
            prefix = "🚨 CRITICAL"
        elif level == config.ALERT_WARNING and config.SHOW_WARNING_ALERTS:
            color = 'yellow'
            prefix = "⚠️  WARNING"
        elif level == config.ALERT_INFO and config.SHOW_INFO_ALERTS:
            color = 'cyan'
            prefix = "ℹ️  INFO"
        else:
            return

        print(self.colorize(f"\n{prefix}: {market_name}", 'bold'))
        print(self.colorize(f"   {message}", color))
        if data:
            for key, value in data.items():
                print(f"   • {key}: {value}")

    def update_price_history(self, token_id: str, price: float):
        """Track price over time for detecting rapid movements"""
        timestamp = time.time()
        self.price_history[token_id].append((timestamp, price))

        # Clean old data
        cutoff = timestamp - config.PRICE_HISTORY_WINDOW
        self.price_history[token_id] = [
            (t, p) for t, p in self.price_history[token_id] if t > cutoff
        ]

    def update_volume_history(self, market_id: str, volume: float):
        """Track volume over time for detecting spikes"""
        timestamp = time.time()
        self.volume_history[market_id].append((timestamp, volume))

        # Clean old data
        cutoff = timestamp - config.VOLUME_HISTORY_WINDOW
        self.volume_history[market_id] = [
            (t, v) for t, v in self.volume_history[market_id] if t > cutoff
        ]

    def get_price_change(self, token_id: str, current_price: float) -> Optional[float]:
        """Calculate price change percentage since last scan"""
        if token_id not in self.price_history or not self.price_history[token_id]:
            return None

        # Get price from beginning of history window
        oldest_price = self.price_history[token_id][0][1]
        if oldest_price == 0:
            return None

        change_percent = ((current_price - oldest_price) / oldest_price) * 100
        return change_percent

    def get_volume_spike(self, market_id: str, current_volume: float) -> Optional[float]:
        """Calculate if current volume is a spike compared to average"""
        if market_id not in self.volume_history or len(self.volume_history[market_id]) < 2:
            return None

        # Calculate average volume from history
        volumes = [v for _, v in self.volume_history[market_id][:-1]]  # Exclude current
        avg_volume = sum(volumes) / len(volumes) if volumes else 0

        if avg_volume == 0:
            return None

        spike_ratio = current_volume / avg_volume
        return spike_ratio

    def analyze_market(self, market: Dict) -> List[Dict]:
        """
        Analyze a single market for unusual activity
        Returns list of alerts detected
        """
        alerts = []
        market_id = market.get('condition_id', 'unknown')
        market_name = market.get('question', 'Unknown Market')

        # Get market metrics
        volume = float(market.get('volume', 0))
        liquidity = float(market.get('liquidity', 0))

        # Skip low-volume markets
        if volume < config.MIN_MARKET_VOLUME:
            return alerts

        # Update volume history and check for spikes
        self.update_volume_history(market_id, volume)
        volume_spike = self.get_volume_spike(market_id, volume)

        if volume_spike and volume_spike >= config.VOLUME_SPIKE_MULTIPLIER:
            alerts.append({
                'level': config.ALERT_WARNING,
                'message': f"Volume spike detected: {volume_spike:.1f}x normal",
                'data': {
                    'current_volume': f"${volume:,.0f}",
                    'spike_ratio': f"{volume_spike:.1f}x"
                }
            })

        # Check for large positions (top holders)
        try:
            holders = self.api.get_market_holders(market_id, limit=10)
            if holders:
                self._analyze_holders(market_name, holders, alerts)
            time.sleep(config.API_REQUEST_DELAY)
        except Exception as e:
            pass  # Skip if holders API fails

        # Check tokens (YES/NO outcomes) for price movements
        tokens = market.get('tokens', [])
        for token in tokens:
            token_id = token.get('token_id')
            outcome = token.get('outcome', 'Unknown')
            price = float(token.get('price', 0))

            if not token_id:
                continue

            # Update price history
            self.update_price_history(token_id, price)

            # Check for rapid price changes
            price_change = self.get_price_change(token_id, price)
            if price_change is not None:
                if abs(price_change) >= config.EXTREME_PRICE_CHANGE_PERCENT:
                    alerts.append({
                        'level': config.ALERT_CRITICAL,
                        'message': f"EXTREME price movement on {outcome}: {price_change:+.1f}%",
                        'data': {
                            'outcome': outcome,
                            'current_price': f"{price:.3f}",
                            'change': f"{price_change:+.1f}%"
                        }
                    })
                elif abs(price_change) >= config.RAPID_PRICE_CHANGE_PERCENT:
                    alerts.append({
                        'level': config.ALERT_WARNING,
                        'message': f"Rapid price movement on {outcome}: {price_change:+.1f}%",
                        'data': {
                            'outcome': outcome,
                            'current_price': f"{price:.3f}",
                            'change': f"{price_change:+.1f}%"
                        }
                    })

        # Check for large recent trades
        try:
            large_trades = self.api.detect_recent_large_trades(
                market_id,
                min_size_usd=config.LARGE_TRADE_MIN_USD,
                lookback_minutes=config.SCAN_INTERVAL // 60 + 1
            )
            if large_trades:
                self._analyze_large_trades(market_name, large_trades, alerts)
            time.sleep(config.API_REQUEST_DELAY)
        except Exception as e:
            pass  # Skip if trades API fails

        return alerts

    def _analyze_holders(self, market_name: str, holders: List[Dict], alerts: List[Dict]):
        """Analyze top holders for concentration and large positions"""
        if not holders:
            return

        total_positions = sum(float(h.get('amount', 0)) for h in holders)

        for i, holder in enumerate(holders[:5]):  # Top 5 holders
            wallet = holder.get('address', 'unknown')
            amount = float(holder.get('amount', 0))
            outcome = holder.get('outcome', 'Unknown')

            # Calculate position value (rough estimate)
            # This is simplified - actual value depends on current price
            position_value = amount  # In practice, multiply by price

            # Check for whale positions
            if position_value >= config.WHALE_POSITION_MIN_USD:
                level = config.ALERT_CRITICAL
                msg = f"🐋 WHALE position detected: #{i+1} holder has ${position_value:,.0f} in {outcome}"

                # Track this wallet
                if wallet not in self.whale_wallets and position_value >= config.AUTO_TRACK_WALLET_MIN_TRADE:
                    self.whale_wallets.add(wallet)
                    self._save_whale_wallet(wallet, position_value)

                alerts.append({
                    'level': level,
                    'message': msg,
                    'data': {
                        'wallet': wallet[:10] + '...',
                        'position_value': f"${position_value:,.0f}",
                        'outcome': outcome,
                        'rank': f"#{i+1}"
                    }
                })

            # Check for concentration
            if total_positions > 0:
                concentration = amount / total_positions
                if concentration >= config.TOP_HOLDER_CONCENTRATION:
                    alerts.append({
                        'level': config.ALERT_WARNING,
                        'message': f"High concentration: Top holder owns {concentration*100:.1f}% of {outcome}",
                        'data': {
                            'concentration': f"{concentration*100:.1f}%",
                            'wallet': wallet[:10] + '...'
                        }
                    })

    def _analyze_large_trades(self, market_name: str, trades: List[Dict], alerts: List[Dict]):
        """Analyze large trades for unusual patterns"""
        for trade in trades:
            wallet = trade.get('user', 'unknown')
            size = float(trade.get('size', 0))
            price = float(trade.get('price', 0))
            side = trade.get('side', 'unknown')
            value = size * price

            # Check for whale trades
            if value >= config.WHALE_TRADE_MIN_USD:
                level = config.ALERT_CRITICAL

                # Check for contrarian bets (low probability YES or high probability NO)
                is_contrarian = False
                if side == 'BUY' and price < config.LOW_PROBABILITY_THRESHOLD:
                    is_contrarian = True
                    contrarian_msg = f"at LOW price {price:.3f} (high conviction YES)"
                elif side == 'SELL' and price > config.HIGH_PROBABILITY_THRESHOLD:
                    is_contrarian = True
                    contrarian_msg = f"at HIGH price {price:.3f} (high conviction NO)"

                msg = f"🐋 WHALE trade: ${value:,.0f} {side}"
                if is_contrarian:
                    msg += f" {contrarian_msg} - POTENTIAL INSIDER?"
                    level = config.ALERT_CRITICAL

                # Track this wallet
                if wallet not in self.whale_wallets and value >= config.AUTO_TRACK_WALLET_MIN_TRADE:
                    self.whale_wallets.add(wallet)
                    self._save_whale_wallet(wallet, value)

                alerts.append({
                    'level': level,
                    'message': msg,
                    'data': {
                        'wallet': wallet[:10] + '...',
                        'trade_value': f"${value:,.0f}",
                        'side': side,
                        'price': f"{price:.3f}",
                        'size': f"{size:,.0f}"
                    }
                })

    def _save_whale_wallet(self, wallet: str, trade_value: float):
        """Save newly discovered whale wallet to file"""
        whale_data = {
            'address': wallet,
            'discovered_at': datetime.now().isoformat(),
            'discovery_trade_value': trade_value
        }

        # Load existing whales
        whales = []
        if os.path.exists(config.WHALE_WALLETS_FILE):
            try:
                with open(config.WHALE_WALLETS_FILE, 'r') as f:
                    whales = json.load(f)
            except:
                pass

        # Add new whale
        whales.append(whale_data)

        # Save
        with open(config.WHALE_WALLETS_FILE, 'w') as f:
            json.dumps(whales, indent=2)

    def scan_markets(self):
        """Main scanning loop - check all active markets for unusual activity"""
        print(f"\n🔄 Starting scan at {datetime.now().strftime('%H:%M:%S')}")

        # Fetch active markets
        markets = self.api.get_active_markets_with_volume(min_volume=config.MIN_MARKET_VOLUME)

        if not markets:
            print("   No markets returned from API")
            return

        print(f"   Scanning {len(markets)} markets...")

        alert_count = 0

        # Analyze each market
        for market in markets[:config.MAX_MARKETS_TO_SCAN]:
            market_name = market.get('question', 'Unknown')

            alerts = self.analyze_market(market)

            # Log all alerts
            for alert in alerts:
                self.log_alert(
                    alert['level'],
                    market_name,
                    alert['message'],
                    alert.get('data')
                )
                alert_count += 1

            time.sleep(config.API_REQUEST_DELAY)

        if alert_count == 0:
            print(self.colorize(f"   ✓ Scan complete - no unusual activity detected", 'green'))
        else:
            print(self.colorize(f"\n   ⚡ Scan complete - {alert_count} alerts generated", 'bold'))

        print(f"   Tracked wallets: {len(self.whale_wallets)}")

    def run(self):
        """Main run loop"""
        print("\n" + "="*60)
        print(self.colorize("  POLYMARKET SCANNER - PHASE 1", 'bold'))
        print(self.colorize("  Monitoring for unusual market activity...", 'cyan'))
        print("="*60)

        try:
            while True:
                try:
                    self.scan_markets()
                except Exception as e:
                    print(self.colorize(f"❌ Error during scan: {str(e)}", 'red'))

                print(f"\n   💤 Waiting {config.SCAN_INTERVAL}s until next scan...")
                print("   " + "-"*50)
                time.sleep(config.SCAN_INTERVAL)

        except KeyboardInterrupt:
            print("\n\n" + self.colorize("🛑 Scanner stopped by user", 'yellow'))
            print(f"   Total whale wallets discovered: {len(self.whale_wallets)}")
            print(f"   Alerts saved to: {config.ALERTS_LOG_FILE}")


if __name__ == "__main__":
    scanner = MarketScanner()
    scanner.run()
