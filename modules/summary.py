import discord
from discord.ext import commands
import openai

class Summary(commands.Cog):
    def __init__(self, bot, openai_api_key):
        self.bot = bot
        self.openai_api_key = openai_api_key
        print("Summary cog initialized")

    def timeframe_to_seconds(self, timeframe):

        if not timeframe[:-1]:  # Check if the string is empty
            return None

        time_unit = timeframe[-1].lower()
        # turn this if else ladder into a dictionary
        if time_unit not in ["h", "d", "w", "m", "y"]:
            return None
        d = {"h": 3600, "d": 86400, "w": 604800, "m": 2592000, "y": 31536000}
        return int(timeframe[:-1]) * d[time_unit]
    async def get_summary(self, ctx, timeframe):
        global openai_api_key

        if self.openai_api_key is None:
            await ctx.send(
                "What you think this is free? Set the OpenAI API key with the command `!!setapikey YOUR_API_KEY`")
            return None

    @commands.command(name="whatsbeengoingoninthepast")
    async def whatsbeengoingoninthepast(self, ctx, timeframe: str):
        if self.timeframe_to_seconds(timeframe) is None:
            await ctx.send("Invalid timeframe format. Please use a number followed by h, d, w, m, or y.")
            return

        summary = await self.get_summary(ctx, timeframe)
        await ctx.send(summary)