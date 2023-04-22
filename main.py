# import asyncio
# import datetime
# import os
# import re
#
# import discord
# import openai
# import requests
# from discord.ext import commands
#
# openai_api_key = None
# openai.api_key = "YOUR_OPENAI_API_KEY"
# intents = discord.Intents.default()
# intents.messages = True
# intents.message_content = True
# intents.members = True
#
# bot = commands.Bot(command_prefix='!!', intents=intents)
# bot = commands.Bot(command_prefix="!!", intents=intents, help_command=None)
#
#
# def timeframe_to_seconds(timeframe):
#     if not timeframe[:-1]:  # Check if the string is empty
#         return None
#
#     time_unit = timeframe[-1].lower()
#     #turn this if else ladder into a dictionary
#     if time_unit not in ["h", "d", "w", "m", "y"]:
#         return None
#     d = {"h": 3600, "d": 86400, "w": 604800, "m": 2592000, "y": 31536000}
#     return int(timeframe[:-1]) * d[time_unit]
#
#
# @bot.command(name="setapikey")
# async def setapikey(ctx, api_key: str):
#     global openai_api_key
#     openai_api_key = api_key
#     openai.api_key = openai_api_key
#     await ctx.send("OpenAI API key has been set.")
#
#
# async def get_messages_in_timeframe(channel, timeframe):
#     timeframe_seconds = timeframe_to_seconds(timeframe)
#     if timeframe_seconds is None:
#         return []
#
#     now = datetime.datetime.utcnow()
#     start_time = now - datetime.timedelta(seconds=timeframe_seconds)
#
#     messages = []
#     async for message in channel.history(after=start_time):
#         if message.author != bot.user:
#             messages.append(message)
#
#     return messages
#
#
# async def get_summary(ctx, timeframe):
#     global openai_api_key
#
#     if openai_api_key is None:
#         await ctx.send(
#             "What you think this is free? Set the OpenAI API key with the command `!!setapikey YOUR_API_KEY`")
#         return None
#
#     messages = await get_messages_in_timeframe(ctx.channel, timeframe)
#     message_text = " ".join([msg.content for msg in messages])
#
#     prompt = f"Make a summary of the following discord conversation that does its best to include everything that has transpired:\n\n{message_text}\n\nSummary:"
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=400,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )
#
#     summary = response.choices[0].text.strip()
#     return summary
#
#
# @bot.command(name="whatsbeengoingoninthepast")
# async def whatsbeengoingoninthepast(ctx, timeframe: str):
#     if timeframe_to_seconds(timeframe) is None:
#         await ctx.send("Invalid timeframe format. Please use a number followed by h, d, w, m, or y.")
#         return
#
#     summary = await get_summary(ctx, timeframe)
#     await ctx.send(summary)
#
#
# async def generate_nickname(message_text):
#     global openai_api_key
#
#     if openai_api_key is None:
#         return "what you think this is free?"
#
#     prompt = f"Generate a creative and relevant Discord nickname based on the following user's message history:\n\n{message_text}\n\nNickname:"
#
#     response = await asyncio.to_thread(
#         openai.Completion.create,
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=50,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )
#
#     nickname = response.choices[0].text.strip()
#     return nickname
#
#
# @bot.command(name="generate_nickname")
# async def generate_nickname_command(ctx, input_string: str):
#     # Extract the channel mention (if any) using a regular expression
#     channel_pattern = re.compile(r"<#(\d+)>")
#     channel_mention = channel_pattern.search(input_string)
#
#     if channel_mention:
#         channel_id = int(channel_mention.group(1))
#         channel = ctx.guild.get_channel(channel_id)
#         user_name = input_string[:channel_mention.start()].strip()
#     else:
#         channel = ctx.channel
#         user_name = input_string.strip()
#
#     if channel is None:
#         await ctx.send(f"Channel not found.")
#         return
#
#     await ctx.send(f"Got you fam, I'm using {channel} ")
#
#     user = None
#     for member in ctx.guild.members:
#         if (user_name in member.display_name) or (member.nick and user_name in member.nick):
#             user = member
#             break
#
#     if user is None:
#         await ctx.send(f"User '{user_name}' not found.")
#         return
#
#     messages = await get_messages_in_timeframe(channel, "1m")
#     user_messages = [msg.content for msg in messages if msg.author == user]
#     message_text = " ".join(user_messages)
#
#     nickname = await generate_nickname(message_text)
#     await ctx.send(f"{user.display_name}? more like {nickname}")
#
#
# # Function to generate image from text
# async def create_image(text):
#     image_path = 'generated_image.png'
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {openai_api_key}',
#     }
#     data = {
#         'prompt': text,
#         'n': 1,
#         'size': '256x256',
#     }
#     response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, json=data)
#     response.raise_for_status()
#     image_url = response.json()['data'][0]['url']
#
#     with open(image_path, 'wb') as f:
#         f.write(requests.get(image_url).content)
#
#     return image_path
#
#
# # Listen for "visualize" command
# @bot.command(name='visualize')
# async def visualize(ctx, *, text):
#     image_path = await create_image(text)
#     with open(image_path, 'rb') as img_file:
#         # Create and send Discord file
#         discord_file = discord.File(fp=img_file, filename='visualized_text.png')
#         await ctx.send(file=discord_file)
#
#     # Remove the generated image file
#     os.remove(image_path)
#
#
# @bot.event
# async def on_ready():
#     print(f"{bot.user.name} is connected to Discord!")
#
#
# async def generate_roast(user_name, messages):
#     prompt = f"Based on these messages from {user_name}, create a funny and playful roast remember to exclude any " \
#              f"names mention and focus on topics:\n{messages}\nRoast:"
#
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=150,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )
#
#     joke = response.choices[0].text.strip()
#     return joke
#
#
# class DisplayNameMemberConverter(commands.MemberConverter):
#     async def convert(self, ctx, argument):
#         for member in ctx.guild.members:
#             if member.display_name.lower() == argument.lower():
#                 return member
#         raise commands.MemberNotFound(argument)
#
#
# @bot.command(name='roast')
# async def roast(ctx, *, user_name: str):
#     try:
#         # await ctx.send([member.display_name for member in ctx.guild.members])
#         user = await DisplayNameMemberConverter().convert(ctx, user_name)
#
#     except commands.MemberNotFound:
#         await ctx.send(f"User {user_name} not found.")
#         return
#
#     messages = []
#     async for message in ctx.channel.history(limit=1000):
#         if message.author == user:
#             messages.append(message.content)
#
#     if not messages:
#         await ctx.send(f"I couldn't find any messages from {user.mention}.")
#         return
#
#     # Combine last 40 messages or less
#     messages = "\n".join(messages[:40])
#
#     joke = await generate_roast(user_name, messages)
#     await ctx.send(joke)
#
#
# # Help command
# @bot.command(name="help")
# async def help_command(ctx):
#     embed = discord.Embed(
#         title="Help",
#         description="List of commands available:",
#         color=0x00FF00,)
#
#     embed.add_field(name="!!setapikey <api_key>", value="Set the OpenAI API key.", inline=False)
#     embed.add_field(name="!!whatsbeengoingoninthepast <timeframe>",
#                     value="Get a summary of the conversation in the past specified timeframe.", inline=False)
#     embed.add_field(name="!!generate_nickname <input_string>",
#                     value="Generate a relevant Discord nickname for a user based on their message history.",
#                     inline=False)
#     embed.add_field(name="!!visualize <text>", value="Generate an image from the provided text.", inline=False)
#     embed.add_field(name="!!roast <user_name>", value="Roasts user based on their last 40 messages", inline=False)
#
#     await ctx.send(embed=embed)
#
#
# bot.run("")

