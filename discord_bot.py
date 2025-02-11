import os
import asyncio
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from login_test import login  # Ensure login() returns a valid Shioaji API object
from shioaji.constant import Action, StockPriceType, OrderType, QuoteType, QuoteVersion
import time
from shioaji import TickFOPv1, BidAskFOPv1, Exchange
from threading import Thread, Event

# Load environment variables from .env file
load_dotenv()

# Get Discord token and channel ID from environment
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise Exception("DISCORD_TOKEN is not set in your environment.")

DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
if not DISCORD_CHANNEL_ID:
    raise Exception("DISCORD_CHANNEL_ID is not set in your environment.")

# Log in to Shioaji API
api = login()
if api is None:
    raise Exception("Failed to log in to Shioaji API.")

# Set up Discord bot intents – enabling message content is required for processing commands
intents = discord.Intents.default()
intents.message_content = True

# Create the bot instance with a command prefix and the specified intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user.name} (ID: {bot.user.id})')
    # Start a background task to update the bot's status every 60 seconds
    update_status.start()
    # Start the tick subscription in a separate thread so that it does not block Discord's event loop
    start_tick_subscription()

@tasks.loop(seconds=60)
async def update_status():
    # Update the bot's status every 60 seconds
    await bot.change_presence(activity=discord.Game("with Python"))
    print("Updated bot status.")

# Simple ping command to test responsiveness
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

# A greeting command
@bot.command(name="hello")
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}! Hope you're having a great day.")

# Command named "2330" to get snapshot data for stock 2330
@bot.command(name="2330")
async def stock_snapshot(ctx):
    result = api.snapshots([api.Contracts.Stocks['2330']])
    
    # Debug prints for inspection
    print("Type of result:", type(result))
    print("Result content:", result)
    
    message_lines = []
    
    if isinstance(result, (tuple, list)):
        for index, item in enumerate(result):
            try:
                item_repr = item.model_dump()  # Use model_dump() for Pydantic v2 models
            except AttributeError:
                item_repr = str(item)
            message_lines.append(f"Snapshot {index}: {item_repr}")
    else:
        try:
            message_lines.append(str(result.model_dump()))
        except AttributeError:
            message_lines.append(str(result))
    
    response = "\n".join(message_lines)
    await ctx.send(f"2330 Snapshot:\n{response}")

# Parameterized command: !stock <stock_number>
@bot.command(name="stock")
async def stock_param(ctx, stock_number: str):
    """
    Fetches and displays snapshot data for a given stock number.
    Usage: !stock 2330
    """
    try:
        contract = api.Contracts.Stocks[stock_number]
    except KeyError:
        await ctx.send(f"Stock {stock_number} not found.")
        return

    try:
        result = api.snapshots([contract])
    except Exception as e:
        await ctx.send(f"Error fetching snapshot for {stock_number}: {e}")
        return

    print("Type of result:", type(result))
    print("Result content:", result)
    
    message_lines = []
    if isinstance(result, (tuple, list)):
        for index, item in enumerate(result):
            try:
                item_repr = item.model_dump()
            except AttributeError:
                item_repr = str(item)
            message_lines.append(f"Snapshot {index}: {item_repr}")
    else:
        try:
            message_lines.append(str(result.model_dump()))
        except AttributeError:
            message_lines.append(str(result))
    
    response = "\n".join(message_lines)
    await ctx.send(f"{stock_number} Snapshot:\n{response}")

# Command to display basic server info using an embed
@bot.command(name="server")
async def server_info(ctx):
    server = ctx.guild
    embed = discord.Embed(title=f"Server Info - {server.name}", color=discord.Color.blue())
    embed.add_field(name="Server ID", value=server.id, inline=False)
    embed.add_field(name="Member Count", value=server.member_count, inline=False)
    await ctx.send(embed=embed)

# Simple error handler for commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I didn't understand that command.")
    else:
        print(f"Error: {error}")
        await ctx.send("An error occurred.")

# Function to start tick subscription in a separate thread
def start_tick_subscription():
    def subscribe_ticks():
        # Subscribe to tick data for stock "2330"
        api.quote.subscribe(
            api.Contracts.Stocks["2330"],
            quote_type=QuoteType.Tick,
            version=QuoteVersion.v1
        )
        print("Subscribed to tick data for stock 2330.")
        
        @api.on_tick_stk_v1()
        def tick_callback(exchange: Exchange, tick):
            # Check the tick volume and send a Discord message if it meets the condition
            if tick.volume >= 10:
                message = (
                    f"Tick received for stock 2330:\n"
                    f"Exchange: {exchange}\n"
                    f"Volume: {tick.volume}\n"
                    f"Details: {tick}"
                )
                print(message)
                channel = bot.get_channel(int(DISCORD_CHANNEL_ID))
                if channel:
                    asyncio.run_coroutine_threadsafe(channel.send(message), bot.loop)
                else:
                    print("Discord channel not found.")
            else:
                # Optionally log low-volume ticks or other data
                print(f"Tick volume too low: {tick.volume}. Volatility: {tick.high - tick.low}")
        
        # Keep the thread alive
        Event().wait()
    
    tick_thread = Thread(target=subscribe_ticks, daemon=True)
    tick_thread.start()

# Run the Discord bot
bot.run(TOKEN)
