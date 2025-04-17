#imports
import asyncio
import discord
from discord.ext import commands
import openai
from openai import OpenAI
import requests
import json
import os


#keep this stuff in a .env file do not hardcode lol
USER_TOKEN = "NjcyODM3MjIwOTUxOTE2NTQ1.Gny3oR.KMtODQXfiDWm7IY0WXa2BUrqdGKQh9yeNzC_oY"
Morphine_Server_ID = 1053388723737337967
Morphine_Channel_ID = 1060658654350688447
Personal_Server_ID = 990575817115463770
Personal_Channel_ID = 990575817115463773
TARGET_SERVER_ID = Personal_Server_ID
TARGET_CHANNEL_ID = Personal_Channel_ID
TRADIER_TOKEN = "cEZBR2y14lCRz4FvT6gsHZqWPY6c"
TRADIER_ACCOUNT_ID = "VA81758002"


# Configuration file path
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

#establishes selfbot
bot = commands.Bot(command_prefix="!", self_bot=True)

#extracts data from messages
def extract_option_data(message_content):
    if "%" in message_content:
        return None
    
    # Configure OpenAI
    api_key = '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'
    if not api_key:
        print("Error: API key not set")
        return None
    
    client = OpenAI(api_key=api_key)
    
    # Create a system prompt that explains what we want to extract
    system_prompt = """
    Extract option trading information from the message. Return a JSON with these fields:
    - symbol: The stock ticker symbol (e.g., "SPY")
    - strike: The strike price as a string (e.g., "400")
    - option_type: "Puts" or "Calls"
    - expiration: The expiration date in MM/DD format (e.g., "3/15")
    - price: The option price as a string with 2 decimal places (e.g., "1.25")
    
    If the message doesn't contain valid option information, return null.
    The message format should be similar to: "$SPY 400 Calls 3/15 $1.25"
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message_content}
            ],
            temperature=0,  # Keep it deterministic
            response_format={ "type": "json_object" }
        )
        
        # Parse the response
        extracted_data = json.loads(response.choices[0].message.content)
        
        if not extracted_data:
            return None
            
        # Process the extracted data similar to the original code
        try:
            day, month = extracted_data['expiration'].split("/")
            month = month.zfill(2)  # ensure two digits
            day = day.zfill(2)
            expiration_occ = "25" + month + day
            
            option_type_letter = "P" if extracted_data['option_type'].lower().startswith("put") else "C"
            
            strike_value = float(extracted_data['strike'])
            strike_occ_int = int(round(strike_value * 1000))
            strike_occ = f"{strike_occ_int:08d}"  # zero-padded to 8 digits
            
            option_symbol = f"{extracted_data['symbol']}{expiration_occ}{option_type_letter}{strike_occ}"
            
            return {
                "option_class": "option",
                "symbol": extracted_data['symbol'],
                "strike": extracted_data['strike'],
                "option_type": extracted_data['option_type'],
                "expiration": extracted_data['expiration'],
                "price": extracted_data['price'],
                "side": "buy_to_open",
                "option_symbol": option_symbol
            }
            
        except Exception as e:
            print(f"Error processing extracted data: {e}")
            return None
            
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

#Sends orders to tradier
async def send_tradier_order(payload):
    url = f"https://sandbox.tradier.com/v1/accounts/{TRADIER_ACCOUNT_ID}/orders"
    headers = {
        'Authorization': f"Bearer {TRADIER_TOKEN}",
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        if response.status_code == 200:
            try: 
                
                json_response = response.json()
                print(f"JSON Response: {json_response}")
                return response.status_code, json_response  # Return status and parsed response
            except ValueError:
                    print("Response is not valid JSON")
                    return response.status_code, None  # Return status with no parsed response
        else:
            print(f"API request failed with status {response.status_code}")
            return response.status_code, None
    except Exception as e:
        print(f"Error sending Tradier API request: {e}")
        return None, None



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Ensure config file exists
    load_config()

@bot.event
async def on_message(message):
    if message.guild and message.channel:
        if message.guild.id == TARGET_SERVER_ID and message.channel.id == TARGET_CHANNEL_ID:
            option_data = extract_option_data(message.content)
            if option_data:
                #print("Waiting 15 minutes due to delayed market data...")
                #await asyncio.sleep(15 * 60)  # 15 minutes = 900 seconds

                try:
                    # Load current configuration
                    config = load_config()
                    
                    # Calculate entry price with user-defined adjustment
                    entry_price = float(option_data['price']) * config['entry_price_adjustment']
                    
                    # Calculate stop loss and take profit based on user preferences
                    stop_loss_percentage = config['stop_loss']['percentage'] / 100
                    take_profit_percentage = config['take_profit']['percentage'] / 100
                    
                    stop_loss = entry_price * (1 - stop_loss_percentage)
                    take_profit = entry_price * (1 + take_profit_percentage)
                    
                    stop_loss_str = f"{stop_loss:.2f}"
                    take_profit_str = f"{take_profit:.2f}"

                    # Calculate position sizing based on user-defined limits
                    min_amount = config['position_size']['min_amount']
                    max_amount = config['position_size']['max_amount']
                    
                    if (entry_price * 100) > max_amount:
                        pos_size = 0  # Skip buying if the contract is too expensive
                    else:
                        max_contracts = max_amount // (entry_price * 100)  # Maximum contracts to stay within max_amount
                        min_contracts = min_amount // (entry_price * 100)  # Minimum contracts to stay above min_amount
                    
                        if min_contracts == 0: 
                            pos_size = max_contracts  # If even 1 contract is above min_amount, take the max possible
                        else:
                            pos_size = max_contracts if max_contracts * (entry_price * 100) <= max_amount else min_contracts
                    
                    pos_size = max(0, pos_size)  # Ensure pos_size is at least 0

                except Exception as e:
                    print(f"Error calculating prices: {e}")
                    stop_loss_str = "0.00"
                    take_profit_str = "0.00"

                # Skip sending order if position size is 0
                if pos_size == 0:
                    print(f"Skipping order - contract price exceeds maximum amount")
                    return

                otoco_payload = {
                    'class': 'otoco',
                    'duration': 'day',
                    # Primary buy order
                    'type[0]': 'limit',
                    'price[0]': option_data['price'],
                    'option_symbol[0]': option_data['option_symbol'],
                    'side[0]': 'buy_to_open',
                    'quantity[0]': str(pos_size) ,
                    # Take profit order
                    'type[1]': 'limit',
                    'price[1]': take_profit_str,
                    'option_symbol[1]': option_data['option_symbol'],
                    'side[1]': 'sell_to_close',
                    'quantity[1]': str(pos_size),
                    # Stop loss order (using stop_limit order type)
                    'type[2]': 'stop_limit',
                    'price[2]': stop_loss_str,  # Limit price for stop order
                    'stop[2]': stop_loss_str,   # Trigger at stop loss price
                    'option_symbol[2]': option_data['option_symbol'],
                    'side[2]': 'sell_to_close',
                    'quantity[2]': pos_size
                }

                print("Sending OTOCO Order:")
                for key, value in otoco_payload.items():
                    print(f"{key}: {value}")
                
                status, response_json = await send_tradier_order(otoco_payload)
                if status == 200:
                    print("OTOCO order placed successfully!")
                else:
                    print("OTOCO order failed.")
            else:
                print("Message did not match the expected option order format.")

    
try:
    bot.run(USER_TOKEN)
except Exception as e:
    print(f"Error: {e}")