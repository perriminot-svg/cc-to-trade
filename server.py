# server.py
# Flask webhook server for TradingView -> CapitalCore integration
from flask import Flask, request, jsonify
from client import open_position, close_position

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """Root endpoint to verify server is running"""
    return jsonify({
        "status": "online",
        "message": "CapitalCore TradingView Webhook Server",
        "endpoints": {
            "/webhook": "POST - Receive TradingView alerts",
            "/health": "GET - Health check"
        }
    }), 200

@app.route("/webhook", methods=["GET"])
def webhook_info():
    """Info endpoint when accessed via browser"""
    return jsonify({
        "error": "This endpoint only accepts POST requests from TradingView",
        "example_buy": {
            "action": "buy",
            "symbol": "EURUSD_1",
            "volume": "0.01",
            "stop_loss": 0,
            "take_profit": 0
        },
        "example_sell": {
            "action": "sell",
            "symbol": "EURUSD_1",
            "volume": "0.01",
            "stop_loss": 0,
            "take_profit": 0
        },
        "example_close": {
            "action": "close",
            "position_id": "446148"
        }
    }), 405

@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Webhook endpoint for receiving TradingView alerts.
    
    Expected JSON formats:
    
    1. Open BUY position:
    {
        "action": "buy",
        "symbol": "EURUSD_1",
        "volume": "0.01",
        "stop_loss": 0,
        "take_profit": 0
    }
    
    2. Open SELL position:
    {
        "action": "sell",
        "symbol": "EURUSD_1",
        "volume": "0.01",
        "stop_loss": 0,
        "take_profit": 0
    }
    
    3. Close position:
    {
        "action": "close",
        "position_id": "446148"
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
        
        action = data.get("action", "").lower()
        
        # Open BUY position
        if action == "buy":
            symbol = data.get("symbol")
            volume = float(data.get("volume", 0.01))
            sl = float(data.get("stop_loss", 0))
            tp = float(data.get("take_profit", 0))
            
            if not symbol:
                return jsonify({
                    "status": "error",
                    "message": "Missing required field: symbol"
                }), 400
            
            result = open_position(symbol, "Buy", volume, sl, tp)
            return jsonify({
                "status": "success",
                "action": "buy",
                "symbol": symbol,
                "volume": volume,
                "result": result
            })
        
        # Open SELL position
        elif action == "sell":
            symbol = data.get("symbol")
            volume = float(data.get("volume", 0.01))
            sl = float(data.get("stop_loss", 0))
            tp = float(data.get("take_profit", 0))
            
            if not symbol:
                return jsonify({
                    "status": "error",
                    "message": "Missing required field: symbol"
                }), 400
            
            result = open_position(symbol, "Sell", volume, sl, tp)
            return jsonify({
                "status": "success",
                "action": "sell",
                "symbol": symbol,
                "volume": volume,
                "result": result
            })
        
        # Close position
        elif action == "close":
            position_id = data.get("position_id")
            volume = float(data.get("volume", 0.01))
            
            if not position_id:
                return jsonify({
                    "status": "error",
                    "message": "Missing required field: position_id"
                }), 400
            
            result = close_position(position_id, volume)
            return jsonify({
                "status": "success",
                "action": "close",
                "position_id": position_id,
                "result": result
            })
        
        else:
            return jsonify({
                "status": "error",
                "message": f"Unknown action: {action}. Use 'buy', 'sell', or 'close'"
            }), 400
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
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
