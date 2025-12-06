# client.py
# CapitalCore trading API client

import requests
from config import COMMON_HEADERS, TRADE_BASE

OPEN_URL = f"{TRADE_BASE}/open-order"
CLOSE_URL = f"{TRADE_BASE}/close-many-positions"


def open_position(symbol, side, volume, sl=0, tp=0, comment="-"):
    """
    Open a new trading position.
    
    Args:
        symbol: Trading symbol (e.g., "SILVER", "EURUSD")
        side: "Buy" or "Sell"
        volume: Position size (e.g., 0.01)
        sl: Stop loss price (optional, default 0)
        tp: Take profit price (optional, default 0)
        comment: Order comment (optional)
    
    Returns:
        JSON response from server or None if request fails
    """
    payload = {
        "symbol": symbol,
        "type": side,
        "volume": volume,
        "stop_loss": sl,
        "take_profit": tp,
        "comment": comment
    }
    
    try:
        r = requests.post(OPEN_URL, headers=COMMON_HEADERS, json=payload, timeout=10)
        print(f"\n[OPEN POSITION] {symbol} {side} {volume}")
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}\n")
        
        return r.json() if r.text else {"status_code": r.status_code}
    except Exception as e:
        print(f"Error opening position: {e}")
        return {"error": str(e)}


def close_position(ticket, volume):
    """
    Close an existing trading position.
    
    Args:
        ticket: Position ticket ID
        volume: Volume to close (must match or be less than position volume)
    
    Returns:
        JSON response from server or None if request fails
    """
    payload = {
        "positions": [
            {
                "ticket": ticket,
                "volume": volume
            }
        ]
    }
    
    try:
        r = requests.post(CLOSE_URL, headers=COMMON_HEADERS, json=payload, timeout=10)
        print(f"\n[CLOSE POSITION] Ticket: {ticket}, Volume: {volume}")
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}\n")
        
        return r.json() if r.text else {"status_code": r.status_code}
    except Exception as e:
        print(f"Error closing position: {e}")
        return {"error": str(e)}
