import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="commandname", description="My first application Command")
async def first_command(interaction):
    await interaction.response.send_message("Hello!")


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


client.run("")
# bot = interactions.Client(token="MTA5NTgwNTk0MjMwMzU2ODAxMw.GJRv4W.kYvz79vdc7jZsF949fLEvAXc5GHz9CmLVUbRUQ")
# bot = interactions.Client(
#     token=""
# )


# @bot.command()
# async def my_first_command(ctx: interactions.CommandContext):
#     """This is the first command I made!"""
#     await ctx.send("Hi there!")
#
#
# bot.start()
