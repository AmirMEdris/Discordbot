import discord
from discord.ext import commands
import openai
import datetime


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

    async def get_messages_in_timeframe(self, channel, timeframe):
        timeframe_seconds = self.timeframe_to_seconds(timeframe)
        if timeframe_seconds is None:
            return []

        now = datetime.datetime.utcnow()
        start_time = now - datetime.timedelta(seconds=timeframe_seconds)

        messages = []
        async for message in channel.history(after=start_time):
            if message.author != self.bot.user:
                messages.append(message)

        return messages

    async def get_summary(self, ctx, timeframe):
        global openai_api_key

        if self.openai_api_key is None:
            await ctx.send(
                "What you think this is free? Set the OpenAI API key with the command `!!setapikey YOUR_API_KEY`")
            return None
        messages = await self.get_messages_in_timeframe(ctx.channel, timeframe)
        message_text = " ".join([msg.content for msg in messages])

        prompt = f"Make a summary of the following discord conversation that does its best to include everything that has transpired:\n\n{message_text}\n\nSummary:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=400,
            n=1,
            stop=None,
            temperature=0.7,
        )

        summary = response.choices[0].text.strip()
        return summary

    @commands.command(name="whatsbeengoingoninthepast")
    async def whatsbeengoingoninthepast(self, ctx, timeframe: str):
        if self.timeframe_to_seconds(timeframe) is None:
            await ctx.send("Invalid timeframe format. Please use a number followed by h, d, w, m, or y.")
            return

        summary = await self.get_summary(ctx, timeframe)
        await ctx.send(summary)
