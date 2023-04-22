import discord
from discord.ext import commands
import openai
import datetime
from modules.membercvtr import DisplayNameMemberConverter



class Help(commands.Cog):
    def __init__(self, bot, openai_api_key):
        self.bot = bot
        self.openai_api_key = openai_api_key
        print("Help cog initialized")

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="Help",
            description="List of commands available:",
            color=0x00FF00,)

        embed.add_field(name="!!setapikey <api_key>", value="Set the OpenAI API key.", inline=False)
        embed.add_field(name="!!whatsbeengoingoninthepast <timeframe>",
                        value="Get a summary of the conversation in the past specified timeframe.", inline=False)
        embed.add_field(name="!!generate_nickname <input_string>",
                        value="Generate a relevant Discord nickname for a user based on their message history.",
                        inline=False)
        embed.add_field(name="!!visualize <text>", value="Generate an image from the provided text.", inline=False)
        embed.add_field(name="!!roast <user_name>", value="Roasts user based on their last 40 messages", inline=False)

        await ctx.send(embed=embed)
