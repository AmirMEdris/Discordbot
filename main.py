
import asyncio
import os
import openai
import discord
from discord.ext import commands
import datetime
from typing import Optional
from discord import TextChannel
import re
from discord.ext.commands import Greedy

openai_api_key = None
openai.api_key = "YOUR_OPENAI_API_KEY"
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!!", intents=intents)


def timeframe_to_seconds(timeframe):
    if not timeframe[:-1]:  # Check if the string is empty
        return None

    time_unit = timeframe[-1].lower()
    time_value = int(timeframe[:-1])
    if time_unit == "h":
        return time_value * 3600
    elif time_unit == "d":
        return time_value * 86400
    elif time_unit == "w":
        return time_value * 604800
    elif time_unit == "m":
        return time_value * 2592000
    elif time_unit == "y":
        return time_value * 31536000
    else:
        return None


@bot.command(name="setapikey")
async def setapikey(ctx, api_key: str):
    global openai_api_key
    openai_api_key = api_key
    openai.api_key = openai_api_key
    await ctx.send("OpenAI API key has been set.")


async def get_messages_in_timeframe(channel, timeframe):
    timeframe_seconds = timeframe_to_seconds(timeframe)
    if timeframe_seconds is None:
        return []

    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(seconds=timeframe_seconds)

    messages = []
    async for message in channel.history(after=start_time):
        if message.author != bot.user:
            messages.append(message)

    return messages


async def get_summary(ctx, timeframe):
    global openai_api_key

    if openai_api_key is None:
        await ctx.send(
            "What you think this is free? Set the OpenAI API key with the command `!!setapikey YOUR_API_KEY` before using this command.")
        return None

    messages = await get_messages_in_timeframe(ctx.channel, timeframe)
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


@bot.command(name="whatsbeengoingoninthepast")
async def whatsbeengoingoninthepast(ctx, timeframe: str):
    if timeframe_to_seconds(timeframe) is None:
        await ctx.send("Invalid timeframe format. Please use a number followed by h, d, w, m, or y.")
        return

    summary = await get_summary(ctx, timeframe)
    await ctx.send(summary)


async def generate_nickname(message_text):
    global openai_api_key

    if openai_api_key is None:
        return "what you think this is free?"

    prompt = f"Generate a creative and relevant Discord nickname based on the following user's message history:\n\n{message_text}\n\nNickname:"

    response = await asyncio.to_thread(
        openai.Completion.create,
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    nickname = response.choices[0].text.strip()
    return nickname


from discord import TextChannel


@bot.command(name="generate_nickname")
async def generate_nickname_command(ctx, input_string: str):
    # Extract the channel mention (if any) using a regular expression
    channel_pattern = re.compile(r"<#(\d+)>")
    channel_mention = channel_pattern.search(input_string)

    if channel_mention:
        channel_id = int(channel_mention.group(1))
        channel = ctx.guild.get_channel(channel_id)
        user_name = input_string[:channel_mention.start()].strip()
    else:
        channel = ctx.channel
        user_name = input_string.strip()

    if channel is None:
        await ctx.send(f"Channel not found.")
        return

    await ctx.send(f"Got you fam, I'm using {channel} ")

    user = None
    for member in ctx.guild.members:
        if (user_name in member.display_name) or (member.nick and user_name in member.nick):
            user = member
            break

    if user is None:
        await ctx.send(f"User '{user_name}' not found.")
        return

    messages = await get_messages_in_timeframe(channel, "1m")
    user_messages = [msg.content for msg in messages if msg.author == user]
    message_text = " ".join(user_messages)

    nickname = await generate_nickname(message_text)
    await ctx.send(f"{user.display_name}? more like {nickname}")


@bot.event
async def on_ready():
    print(f"{bot.user.name} is connected to Discord!")


bot.run("YOUR_BOT_TOKEN")
