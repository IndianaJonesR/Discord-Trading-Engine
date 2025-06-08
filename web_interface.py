from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration file path
CONFIG_FILE = "trading_config.json"

# Default configuration
DEFAULT_CONFIG = {
    "position_size": {
        "min_amount": 100,
        "max_amount": 120
    },
    "stop_loss": {
        "percentage": 20
    },
    "take_profit": {
        "percentage": 30
    },
    "entry_price_adjustment": 1.05  # 5% above market price
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

@app.route('/')
def index():
    return render_template('dark_theme.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(load_config())

@app.route('/api/position', methods=['POST'])
def update_position():
    data = request.get_json()
    config = load_config()
    config['position_size'] = {
        'min_amount': float(data['min_amount']),
        'max_amount': float(data['max_amount'])
    }
    save_config(config)
    return jsonify({'status': 'success'})

@app.route('/api/stop-loss', methods=['POST'])
def update_stop_loss():
    data = request.get_json()
    config = load_config()
    config['stop_loss']['percentage'] = float(data['percentage'])
    save_config(config)
    return jsonify({'status': 'success'})

@app.route('/api/take-profit', methods=['POST'])
def update_take_profit():
    data = request.get_json()
    config = load_config()
    config['take_profit']['percentage'] = float(data['percentage'])
    save_config(config)
    return jsonify({'status': 'success'})

@app.route('/api/entry-adjustment', methods=['POST'])
def update_entry_adjustment():
    data = request.get_json()
    config = load_config()
    # Convert percentage to multiplier (e.g., 5% -> 1.05)
    config['entry_price_adjustment'] = 1 + (float(data['percentage']) / 100)
    save_config(config)
    return jsonify({'status': 'success'})

@app.route('/api/reset', methods=['POST'])
def reset_config():
    save_config(DEFAULT_CONFIG)
    return jsonify({'status': 'success'})

@app.route('/api/trades', methods=['POST'])
def submit_trade():
    """
    Endpoint for manual trade submission from the React frontend.
    This integrates with your existing option trading logic.
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['symbol', 'strike', 'option_type', 'expiration', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'Missing required field: {field}'}), 400
        
        # Here you would integrate with your existing option trading logic from main.py
        # For now, we'll just return a success response
        
        # You could import and use the extract_option_data and send_tradier_order functions
        # from main.py to actually place the trade
        
        trade_data = {
            'symbol': data['symbol'].upper(),
            'strike': data['strike'],
            'option_type': data['option_type'],
            'expiration': data['expiration'],
            'price': data['price']
        }
        
        # TODO: Integrate with your existing trading logic
        # option_data = extract_option_data(f"${trade_data['symbol']} {trade_data['strike']} {trade_data['option_type']} {trade_data['expiration']} ${trade_data['price']}")
        # if option_data:
        #     status, response = await send_tradier_order(payload)
        
        return jsonify({
            'status': 'success', 
            'message': 'Trade submitted successfully',
            'trade': trade_data
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # Ensure the configuration file exists
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True) 