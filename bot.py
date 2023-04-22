#Alternative to using main.py to make the code less cluttered and more readable
#currently doesnt work but i will fix it tommorow

# import discord
# from discord.ext import commands
# import openai
# # from config import openai_api_key, discord_bot_token
# from modules.summary import Summary
#     # , nickname, visualize, roast, help
import discord
from discord.ext import commands
import openai
from modules.summary import Summary

openai.api_key = "openai api key here"
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is online.")
    await bot.add_cog(Summary(bot, openai.api_key))

bot.run("")
