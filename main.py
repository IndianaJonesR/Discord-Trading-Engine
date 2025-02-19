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
        ticker = match.group(1)             # e.g., SPY
        strike_str = match.group(2)         # e.g., "593"
        option_type_text = match.group(3)     # e.g., "Puts" or "Calls"
        expiration_text = match.group(4)      # e.g., "3/3"
        price = match.group(5)              # e.g., "0.68"
        side = "buy_to_open"              # Hardcoded for now

        # Convert expiration "month/day" to OCC format "yymmdd"
        # Assumed year: 2025 -> "25"
        try:
            day, month = expiration_text.split("/")
            month = month.zfill(2)  # ensure two digits
            day = day.zfill(2)
            expiration_occ = "25" + month + day
        except Exception as e:
            print(f"Error processing expiration date: {e}")
            expiration_occ = ""

        # Convert option type to OCC letter: "P" for Puts, "C" for Calls
        if option_type_text.lower().startswith("put"):
            option_type_letter = "P"
        elif option_type_text.lower().startswith("call"):
            option_type_letter = "C"
        else:
            option_type_letter = ""
        
        # Process strike price:
        # Multiply by 1000 and pad with zeros to create an 8-digit number.
        try:
            strike_value = float(strike_str)
            strike_occ_int = int(round(strike_value * 1000))
            strike_occ = f"{strike_occ_int:08d}"  # zero-padded to 8 digits
        except Exception as e:
            print(f"Error processing strike price: {e}")
            strike_occ = ""
        
        # Construct the OCC option symbol
        option_symbol = f"{ticker}{expiration_occ}{option_type_letter}{strike_occ}"
        
        return {
            "ticker": ticker,
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
            #print(f"New message in {message.channel.name}:")
            #print(f"Author: {message.author.name}")
            #print(f"Content: {message.content}\n")

            option_data = extract_option_data(message.content)
            if option_data:
                print("Extracted Option Data:")
                print(f"  Ticker: {option_data['ticker']}")
                print(f"  Strike: {option_data['strike']}")
                print(f"  Option Type: {option_data['option_type']}")
                print(f"  Expiration: {option_data['expiration']}")
                print(f"  Price: {option_data['price']}")
                print(f"  Side: {option_data['side']}")
                print(f"  OCC Option Symbol: {option_data['option_symbol']}")
            else:
                print("Message did not match the expected option order format.")
try:
    bot.run(USER_TOKEN)
except Exception as e:
    print(f"Error: {e}")