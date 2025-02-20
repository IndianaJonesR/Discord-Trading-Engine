import discord
from discord.ext import commands
import asyncio
import re

#keep this stuff in a .env file do not hardcode lol
USER_TOKEN = "NjcyODM3MjIwOTUxOTE2NTQ1.Gny3oR.KMtODQXfiDWm7IY0WXa2BUrqdGKQh9yeNzC_oY"
TARGET_SERVER_ID = 990575817115463770  
TARGET_CHANNEL_ID = 990575817115463773

bot = commands.Bot(command_prefix="!", self_bot=True)

def extract_option_data(message_content):
  
    # Regex to extract: Ticker, Strike, Option Type, Expiration (month/day), and Price
    pattern = r'\$([A-Z]+)\s+(\d+)\s+(Puts|Calls)\s+(\d{1,2}/\d{1,2})\s+\$(\d+\.\d{2})'
    match = re.search(pattern, message_content)
    
    if match:
        option_class = "option"             #hardcoded
        symbol = match.group(1)             # e.g., SPY
        strike_str = match.group(2)         # e.g., "593"
        option_type_text = match.group(3)     # e.g., "Puts" or "Calls"
        expiration_text = match.group(4)      # e.g., "3/3"
        price = match.group(5)              # e.g., "0.68"
        side = "buy_to_open"              # hardcoded for now

        try:
            day, month = expiration_text.split("/")
            month = month.zfill(2)  # ensure two digits
            day = day.zfill(2)
            expiration_occ = "25" + month + day
        except Exception as e:
            print(f"Error processing expiration date: {e}")
            expiration_occ = ""

        if option_type_text.lower().startswith("put"):
            option_type_letter = "P"
        elif option_type_text.lower().startswith("call"):
            option_type_letter = "C"
        else:
            option_type_letter = ""
        
        try:
            strike_value = float(strike_str)
            strike_occ_int = int(round(strike_value * 1000))
            strike_occ = f"{strike_occ_int:08d}"  # zero-padded to 8 digits
        except Exception as e:
            print(f"Error processing strike price: {e}")
            strike_occ = ""
        

        option_symbol = f"{symbol}{expiration_occ}{option_type_letter}{strike_occ}"
    
        return {
            "option_class": option_class,
            "symbol": symbol,
            "strike": strike_str,
            "option_type": option_type_text,
            "expiration": expiration_text,
            "price": price,
            "side": side,
            "option_symbol": option_symbol
        }
    else:
        return None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    
    if message.guild and message.channel:
        if message.guild.id == TARGET_SERVER_ID and message.channel.id == TARGET_CHANNEL_ID:
            option_data = extract_option_data(message.content)
            if option_data:

                try:
                    entry_price = float(option_data['price'])
                    stop_price = entry_price * 0.7
                    stop_price_str = f"{stop_price:.2f}"
                except Exception as e:
                    print(f"Error calculating stop price: {e}")
                    stop_price_str = "0.00"
                
                request_payload = {
                    'class': option_data['option_class'],
                    'symbol': option_data['symbol'],
                    'option_symbol': option_data['option_symbol'],
                    'side': option_data['side'],
                    'quantity': '10',          # Hardcoded quantity
                    'type': 'market',          # Hardcoded order type
                    'duration': 'day',         # Hardcoded duration
                    'price': option_data['price'],
                    'stop': stop_price_str,
                    'tag': 'Order 1'
                }

                print("Data for Tradier API Request:")
                for key, value in request_payload.items():
                    print(f"{key}: {value}")
                
            else:
                print("Message did not match the expected option order format.")
try:
    bot.run(USER_TOKEN)
except Exception as e:
    print(f"Error: {e}")