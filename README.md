# Discord Stock Alert Reader with Web Interface

This project consists of a Discord bot that monitors a specific channel for stock option alerts and automatically places trades based on those alerts. It now includes a web interface for configuring trading parameters.

## Components

1. **Discord Bot (`main.py`)**: Monitors a Discord channel for option alerts and places trades.
2. **Web Interface (`web_interface.py`)**: Provides a user-friendly interface to configure trading parameters.

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure your Discord bot token and other settings in `main.py`.

3. Run the Discord bot:
   ```
   python main.py
   ```

4. In a separate terminal, run the web interface:
   ```
   python web_interface.py
   ```

5. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Web Interface Features

The web interface allows you to configure:

- **Position Size**: Set minimum and maximum position sizes in dollars
- **Stop Loss**: Set the stop loss percentage below entry price
- **Take Profit**: Set the take profit percentage above entry price
- **Entry Price Adjustment**: Set the percentage to adjust entry price above market price

## Configuration

The configuration is stored in `trading_config.json` and is shared between the Discord bot and the web interface. Changes made through the web interface will be immediately reflected in the bot's behavior.

## Default Settings

- Position Size: Min $100, Max $120
- Stop Loss: 20% below entry price
- Take Profit: 30% above entry price
- Entry Price Adjustment: 5% above market price

## Security Note

The web interface is designed to run locally. If you need to access it from other devices on your network, be aware that it doesn't include authentication. Consider adding authentication if deploying in a shared environment.
