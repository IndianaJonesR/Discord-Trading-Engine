import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
import threading
import time

app = Flask(__name__)

# Configuration file path (same as in main.py)
CONFIG_FILE = "trading_config.json"

# Default configuration
DEFAULT_CONFIG = {
    "position_size": {
        "min_amount": 100,
        "max_amount": 120
    },
    "stop_loss": {
        "percentage": 20  # 20% below entry price
    },
    "take_profit": {
        "percentage": 30  # 30% above entry price
    },
    "entry_price_adjustment": 1.05  # 5% above market price
}

# Load configuration from file or create with defaults
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return DEFAULT_CONFIG
    else:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

# Save configuration to file
def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Create the HTML template
with open('templates/index.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading Bot Configuration</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
            padding-top: 2rem;
        }
        .card {
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        .card-header {
            background-color: #4a6bdf;
            color: white;
            border-radius: 15px 15px 0 0 !important;
            font-weight: bold;
        }
        .btn-primary {
            background-color: #4a6bdf;
            border-color: #4a6bdf;
        }
        .btn-primary:hover {
            background-color: #3a5bc9;
            border-color: #3a5bc9;
        }
        .form-control:focus {
            border-color: #4a6bdf;
            box-shadow: 0 0 0 0.25rem rgba(74, 107, 223, 0.25);
        }
        .alert {
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-4">Trading Bot Configuration</h1>
        
        <div class="row">
            <div class="col-md-6 offset-md-3">
                <div class="card">
                    <div class="card-header">
                        Position Size Settings
                    </div>
                    <div class="card-body">
                        <form id="positionForm">
                            <div class="mb-3">
                                <label for="minAmount" class="form-label">Minimum Position Size ($)</label>
                                <input type="number" class="form-control" id="minAmount" min="1" step="1" required>
                            </div>
                            <div class="mb-3">
                                <label for="maxAmount" class="form-label">Maximum Position Size ($)</label>
                                <input type="number" class="form-control" id="maxAmount" min="1" step="1" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Update Position Size</button>
                        </form>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        Stop Loss & Take Profit
                    </div>
                    <div class="card-body">
                        <form id="profitLossForm">
                            <div class="mb-3">
                                <label for="stopLoss" class="form-label">Stop Loss Percentage</label>
                                <input type="number" class="form-control" id="stopLoss" min="1" max="99" step="0.1" required>
                            </div>
                            <div class="mb-3">
                                <label for="takeProfit" class="form-label">Take Profit Percentage</label>
                                <input type="number" class="form-control" id="takeProfit" min="0.1" step="0.1" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Update Stop Loss & Take Profit</button>
                        </form>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        Entry Price Adjustment
                    </div>
                    <div class="card-body">
                        <form id="entryAdjustmentForm">
                            <div class="mb-3">
                                <label for="entryAdjustment" class="form-label">Entry Price Adjustment (%)</label>
                                <input type="number" class="form-control" id="entryAdjustment" min="0.1" step="0.1" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Update Entry Adjustment</button>
                        </form>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        Reset Configuration
                    </div>
                    <div class="card-body">
                        <button id="resetButton" class="btn btn-danger">Reset to Defaults</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
        <div id="alertContainer"></div>
    </div>

    <script>
        // Function to show alerts
        function showAlert(message, type = 'success') {
            const alertContainer = document.getElementById('alertContainer');
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
            alertDiv.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            `;
            alertContainer.appendChild(alertDiv);
            
            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                alertDiv.classList.remove('show');
                setTimeout(() => alertDiv.remove(), 150);
            }, 5000);
        }

        // Load current configuration
        async function loadConfig() {
            try {
                const response = await fetch('/api/config');
                const config = await response.json();
                
                document.getElementById('minAmount').value = config.position_size.min_amount;
                document.getElementById('maxAmount').value = config.position_size.max_amount;
                document.getElementById('stopLoss').value = config.stop_loss.percentage;
                document.getElementById('takeProfit').value = config.take_profit.percentage;
                document.getElementById('entryAdjustment').value = (config.entry_price_adjustment - 1) * 100;
            } catch (error) {
                showAlert('Failed to load configuration', 'danger');
            }
        }

        // Update position size
        document.getElementById('positionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const minAmount = parseFloat(document.getElementById('minAmount').value);
            const maxAmount = parseFloat(document.getElementById('maxAmount').value);
            
            if (minAmount >= maxAmount) {
                showAlert('Minimum amount must be less than maximum amount', 'danger');
                return;
            }
            
            try {
                const response = await fetch('/api/position', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ min_amount: minAmount, max_amount: maxAmount })
                });
                
                if (response.ok) {
                    showAlert('Position size updated successfully');
                } else {
                    showAlert('Failed to update position size', 'danger');
                }
            } catch (error) {
                showAlert('Error updating position size', 'danger');
            }
        });

        // Update stop loss and take profit
        document.getElementById('profitLossForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const stopLoss = parseFloat(document.getElementById('stopLoss').value);
            const takeProfit = parseFloat(document.getElementById('takeProfit').value);
            
            try {
                const response = await fetch('/api/stop-loss', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ percentage: stopLoss })
                });
                
                if (response.ok) {
                    const response2 = await fetch('/api/take-profit', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ percentage: takeProfit })
                    });
                    
                    if (response2.ok) {
                        showAlert('Stop loss and take profit updated successfully');
                    } else {
                        showAlert('Failed to update take profit', 'danger');
                    }
                } else {
                    showAlert('Failed to update stop loss', 'danger');
                }
            } catch (error) {
                showAlert('Error updating stop loss and take profit', 'danger');
            }
        });

        // Update entry adjustment
        document.getElementById('entryAdjustmentForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const adjustment = parseFloat(document.getElementById('entryAdjustment').value);
            
            try {
                const response = await fetch('/api/entry-adjustment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ percentage: adjustment })
                });
                
                if (response.ok) {
                    showAlert('Entry adjustment updated successfully');
                } else {
                    showAlert('Failed to update entry adjustment', 'danger');
                }
            } catch (error) {
                showAlert('Error updating entry adjustment', 'danger');
            }
        });

        // Reset configuration
        document.getElementById('resetButton').addEventListener('click', async () => {
            if (!confirm('Are you sure you want to reset all settings to defaults?')) {
                return;
            }
            
            try {
                const response = await fetch('/api/reset', {
                    method: 'POST'
                });
                
                if (response.ok) {
                    showAlert('Configuration reset to defaults');
                    loadConfig();
                } else {
                    showAlert('Failed to reset configuration', 'danger');
                }
            } catch (error) {
                showAlert('Error resetting configuration', 'danger');
            }
        });

        // Load configuration on page load
        document.addEventListener('DOMContentLoaded', loadConfig);
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    ''')

# API Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(load_config())

@app.route('/api/position', methods=['POST'])
def update_position():
    data = request.json
    min_amount = data.get('min_amount')
    max_amount = data.get('max_amount')
    
    if not min_amount or not max_amount or min_amount >= max_amount:
        return jsonify({'error': 'Invalid position size values'}), 400
    
    config = load_config()
    config['position_size']['min_amount'] = min_amount
    config['position_size']['max_amount'] = max_amount
    
    if save_config(config):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to save configuration'}), 500

@app.route('/api/stop-loss', methods=['POST'])
def update_stop_loss():
    data = request.json
    percentage = data.get('percentage')
    
    if not percentage or percentage <= 0 or percentage >= 100:
        return jsonify({'error': 'Invalid stop loss percentage'}), 400
    
    config = load_config()
    config['stop_loss']['percentage'] = percentage
    
    if save_config(config):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to save configuration'}), 500

@app.route('/api/take-profit', methods=['POST'])
def update_take_profit():
    data = request.json
    percentage = data.get('percentage')
    
    if not percentage or percentage <= 0:
        return jsonify({'error': 'Invalid take profit percentage'}), 400
    
    config = load_config()
    config['take_profit']['percentage'] = percentage
    
    if save_config(config):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to save configuration'}), 500

@app.route('/api/entry-adjustment', methods=['POST'])
def update_entry_adjustment():
    data = request.json
    percentage = data.get('percentage')
    
    if not percentage or percentage <= 0:
        return jsonify({'error': 'Invalid entry adjustment percentage'}), 400
    
    config = load_config()
    config['entry_price_adjustment'] = 1 + (percentage / 100)
    
    if save_config(config):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to save configuration'}), 500

@app.route('/api/reset', methods=['POST'])
def reset_config():
    if save_config(DEFAULT_CONFIG):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to reset configuration'}), 500

if __name__ == '__main__':
    # Ensure config file exists
    load_config()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True) 