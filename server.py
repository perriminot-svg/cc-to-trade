# server.py
# Flask webhook server for TradingView -> CapitalCore integration

from flask import Flask, request, jsonify
from client import open_position, close_position

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Webhook endpoint for receiving TradingView alerts.
    
    Expected JSON formats:
    
    1. Open position:
    {
        "command": "open",
        "symbol": "SILVER",
        "side": "Buy",  // or "Sell"
        "volume": 0.01,
        "sl": 57.718,   // optional
        "tp": 58.718    // optional
    }
    
    2. Close position:
    {
        "command": "close",
        "ticket": 123456,
        "volume": 0.01
    }
    """
    try:
        data = request.get_json(force=True)
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON received"
            }), 400
        
        print("\n[WEBHOOK RECEIVED]")
        print(data)
        
        command = data.get("command")
        
        # Open position
        if command == "open":
            symbol = data.get("symbol")
            side = data.get("side")
            volume = data.get("volume", 0.01)
            sl = data.get("sl", 0)
            tp = data.get("tp", 0)
            
            # Validate required fields
            if not symbol or not side:
                return jsonify({
                    "status": "error",
                    "message": "Missing required fields: symbol and side"
                }), 400
            
            result = open_position(symbol, side, volume, sl, tp)
            return jsonify({
                "status": "ok",
                "command": "open",
                "result": result
            })
        
        # Close position
        elif command == "close":
            ticket = data.get("ticket")
            volume = data.get("volume", 0.01)
            
            if not ticket:
                return jsonify({
                    "status": "error",
                    "message": "Missing required field: ticket"
                }), 400
            
            result = close_position(ticket, volume)
            return jsonify({
                "status": "ok",
                "command": "close",
                "result": result
            })
        
        else:
            return jsonify({
                "status": "error",
                "message": f"Unknown command: {command}. Use 'open' or 'close'"
            }), 400
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({
            "status": "error",
            "exception": str(e)
        }), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    print("=" * 60)
    print("CapitalCore Webhook Server Starting...")
    print("Listening on: http://0.0.0.0:8080/webhook")
    print("=" * 60)
    app.run(host="0.0.0.0", port=8080, debug=False)
