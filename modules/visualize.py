import discord
from discord.ext import commands
import openai
import datetime


class Visualize(commands.Cog):
    def __init__(self, bot, openai_api_key):
        self.bot = bot
        self.openai_api_key = openai_api_key
        print("Visualize cog initialized")
