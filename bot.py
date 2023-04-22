# Alternative to using main.py to make the code less cluttered and more readable
# currently only summary works but all the cogs are successfully loaded

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
from modules.nickname import Nickname
from modules.visualize import Visualize
from modules.roast import Roast
from modules.help import Help

openai.api_key = ""
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


bot.run("")
