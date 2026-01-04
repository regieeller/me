"""
Polymarket API Client
Interfaces with Polymarket's Data API, CLOB API, and Gamma Markets API

Note: This uses the official py-clob-client library + direct API calls
Install: pip install py-clob-client requests
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import time

try:
    from py_clob_client.client import ClobClient
    HAS_CLOB_CLIENT = True
except ImportError:
    HAS_CLOB_CLIENT = False
    print("⚠️  Warning: py-clob-client not installed. Install with: pip install py-clob-client")


class PolymarketAPI:
    """Client for interacting with Polymarket APIs"""

    DATA_API_BASE = "https://data-api.polymarket.com"
    CLOB_API_BASE = "https://clob.polymarket.com"
    GAMMA_API_BASE = "https://gamma-api.polymarket.com"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PolymarketScanner/1.0'
        })

        # Initialize official CLOB client if available
        if HAS_CLOB_CLIENT:
            try:
                self.clob_client = ClobClient(self.CLOB_API_BASE)
            except Exception as e:
                print(f"⚠️  Warning: Could not initialize CLOB client: {e}")
                self.clob_client = None
        else:
            self.clob_client = None

    def _make_request(self, url: str, params: Optional[Dict] = None) -> Dict:
        """Make HTTP request with error handling and rate limiting"""
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request failed: {url} - {str(e)}")
            return {}

    # ==================== GAMMA API (Market Metadata) ====================

    def get_markets(self, limit: int = 100, offset: int = 0, active: bool = True) -> List[Dict]:
        """
        Get list of markets with metadata

        Args:
            limit: Number of markets to return (default 100)
            offset: Pagination offset
            active: Only return active markets (default True)

        Returns:
            List of market objects with metadata
        """
        # Try official CLOB client first (more reliable)
        if self.clob_client:
            try:
                markets = self.clob_client.get_simplified_markets()
                if markets:
                    # Filter for active markets if requested
                    if active:
                        markets = [m for m in markets if m.get('active', False)]
                    return markets[:limit]
            except Exception as e:
                print(f"CLOB client failed, falling back to direct API: {e}")

        # Fallback to direct API call
        url = f"{self.GAMMA_API_BASE}/markets"
        params = {
            'limit': limit,
            'offset': offset,
            'active': str(active).lower()
        }
        response = self._make_request(url, params)
        return response.get('data', []) if isinstance(response, dict) else response

    def get_market(self, condition_id: str) -> Dict:
        """Get detailed information for a specific market"""
        url = f"{self.GAMMA_API_BASE}/markets/{condition_id}"
        return self._make_request(url)

    # ==================== DATA API (Trades, Positions, Holders) ====================

    def get_trades(self,
                   user_address: Optional[str] = None,
                   market: Optional[str] = None,
                   limit: int = 100,
                   offset: int = 0) -> List[Dict]:
        """
        Get trade history

        Args:
            user_address: Filter by specific wallet address
            market: Filter by market condition_id
            limit: Number of trades to return
            offset: Pagination offset

        Returns:
            List of trade objects with size, price, timestamp, wallet address
        """
        url = f"{self.DATA_API_BASE}/trades"
        params = {
            'limit': limit,
            'offset': offset
        }
        if user_address:
            params['user'] = user_address
        if market:
            params['market'] = market

        return self._make_request(url, params)

    def get_user_positions(self, user_address: str) -> List[Dict]:
        """
        Get current positions for a wallet address

        Returns:
            List of positions with size, value, P&L metrics
        """
        url = f"{self.DATA_API_BASE}/positions"
        params = {'user': user_address}
        return self._make_request(url, params)

    def get_market_holders(self, condition_id: str, limit: int = 50) -> List[Dict]:
        """
        Get top holders for a specific market

        This is KEY for detecting large positions/whales

        Args:
            condition_id: Market identifier
            limit: Number of top holders to return

        Returns:
            List of holders with wallet addresses and position sizes
        """
        url = f"{self.DATA_API_BASE}/holders"
        params = {
            'id': condition_id,
            'limit': limit
        }
        return self._make_request(url, params)

    def get_user_activity(self,
                         user_address: str,
                         limit: int = 100,
                         activity_type: Optional[str] = None) -> List[Dict]:
        """
        Get activity stream for a wallet

        Args:
            user_address: Wallet to monitor
            limit: Number of activities to return
            activity_type: Filter by type (TRADE, SPLIT, MERGE, REDEEM, etc.)

        Returns:
            Time-ordered activity feed
        """
        url = f"{self.DATA_API_BASE}/activity"
        params = {
            'user': user_address,
            'limit': limit
        }
        if activity_type:
            params['type'] = activity_type

        return self._make_request(url, params)

    # ==================== CLOB API (Order Book) ====================

    def get_order_book(self, token_id: str) -> Dict:
        """
        Get current order book for a token

        Args:
            token_id: Token identifier

        Returns:
            Order book with bids and asks
        """
        url = f"{self.CLOB_API_BASE}/book"
        params = {'token_id': token_id}
        return self._make_request(url, params)

    def get_midpoint_price(self, token_id: str) -> Optional[float]:
        """Get midpoint price (average of best bid and ask)"""
        url = f"{self.CLOB_API_BASE}/midpoint"
        params = {'token_id': token_id}
        result = self._make_request(url, params)
        return float(result.get('mid', 0)) if result else None

    def get_spread(self, token_id: str) -> Optional[float]:
        """Get spread (difference between best ask and bid)"""
        url = f"{self.CLOB_API_BASE}/spread"
        params = {'token_id': token_id}
        result = self._make_request(url, params)
        return float(result.get('spread', 0)) if result else None

    # ==================== Helper Methods ====================

    def get_active_markets_with_volume(self, min_volume: float = 1000) -> List[Dict]:
        """
        Get active markets filtered by minimum volume
        Useful for focusing on liquid markets where large trades matter
        """
        markets = self.get_markets(limit=500, active=True)
        if not markets:
            return []

        # Filter by volume (if available in response)
        return [m for m in markets if m.get('volume', 0) >= min_volume]

    def detect_recent_large_trades(self,
                                   market: str,
                                   min_size_usd: float = 1000,
                                   lookback_minutes: int = 60) -> List[Dict]:
        """
        Find large trades in a specific market within timeframe

        Args:
            market: Market condition_id
            min_size_usd: Minimum trade size in USD
            lookback_minutes: How far back to look

        Returns:
            List of large trades with wallet addresses
        """
        trades = self.get_trades(market=market, limit=500)
        if not trades:
            return []

        cutoff_time = datetime.now().timestamp() - (lookback_minutes * 60)
        large_trades = []

        for trade in trades:
            # Parse trade data (structure may vary, adjust as needed)
            trade_time = trade.get('timestamp', 0)
            trade_size = float(trade.get('size', 0)) * float(trade.get('price', 0))

            if trade_time >= cutoff_time and trade_size >= min_size_usd:
                large_trades.append(trade)

        return large_trades


if __name__ == "__main__":
    # Quick test
    api = PolymarketAPI()
    print("Testing Polymarket API Client...")

    print("\nFetching active markets...")
    markets = api.get_markets(limit=5)
    if markets:
        print(f"Found {len(markets)} markets")
        if markets:
            print(f"Sample market: {markets[0].get('question', 'N/A')}")
    else:
        print("No markets returned")

    print("\nAPI client ready!")
