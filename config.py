# config.py
# Configuration for CapitalCore webhook server

import os

# Authentication token from your CapitalCore account
AUTH_TOKEN = f"Bearer {os.getenv('AUTH_TOKEN', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Nzg4NiwidXNyIjoiOWtwZXJyaUBnbWFpbC5jb20iLCJmbiI6IlBlcnJpIiwibG4iOiJNaW5vdCIsImFjcyI6eyIyMzUxNyI6ZmFsc2UsIjEyMDMzOTciOnRydWV9LCJpYXQiOjE3NjUwNTA2MzAsImV4cCI6MTc2NTMwOTgzMCwiaXNfZ3Vlc3QiOmZhbHNlfQ.iPkP4Ki1x1ayMIKh_tifZO6aVYVpBnPnqIzldGVeaQo')}"

# Your CapitalCore account ID
ACCOUNT_ID = os.getenv('ACCOUNT_ID', '1203397')

# API endpoints
API_BASE = "https://pro.capitalcore.com/api/v1" 
TRADE_BASE = f"{API_BASE}/user/account/1203397/trade/open-order"

# Common headers for all requests
COMMON_HEADERS = {
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Nzg4NiwidXNyIjoiOWtwZXJyaUBnbWFpbC5jb20iLCJmbiI6IlBlcnJpIiwibG4iOiJNaW5vdCIsImFjcyI6eyIyMzUxNyI6ZmFsc2UsIjEyMDMzOTciOnRydWV9LCJpYXQiOjE3NjUwNDc2ODEsImV4cCI6MTc2NTMwNjg4MSwiaXNfZ3Vlc3QiOmZhbHNlfQ.ffC7iyyvx-1Q46OKYMKtKwj6K_oMEJCuDmEd0WXtdYI",
    "Content-Type": "application/json",
    "origin": "https://pro.capitalcore.com",
    "referer": "https://pro.capitalcore.com/?",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}





