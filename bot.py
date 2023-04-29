import openai
import discord
from modules.summary import Summary
from discord.ext import commands
from modules.nickname import Nickname
from modules.visualize import Visualize
from modules.roast import Roast
from modules.help import Help
import yaml

# Read config.yaml and get the openai_key and bot_token
with open("config.yaml", "r") as file:
    config_data = yaml.safe_load(file)

# Set OpenAI API key
openai.api_key = config_data.get("openai_key")
bot_token = config_data.get("bot_token")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is online.")
    await bot.add_cog(Summary(bot, openai.api_key))
    await bot.add_cog(Help(bot, openai.api_key))
    await bot.add_cog(Nickname(bot, openai.api_key))
    await bot.add_cog(Visualize(bot, openai.api_key))
    await bot.add_cog(Roast(bot, openai.api_key))
#add speaking function using elevenlabs
bot.run(bot_token)

