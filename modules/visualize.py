
import os

import discord
import requests
from discord.ext import commands
import openai
import datetime


class Visualize(commands.Cog):
    def __init__(self, bot, openai_api_key):
        self.bot = bot
        self.openai_api_key = openai_api_key
        print("Visualize cog initialized")

    async def create_image(self, text):
        image_path = 'generated_image.png'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.openai_api_key}',
        }
        data = {
            'prompt': text,
            'n': 1,
            'size': '256x256',
        }
        response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, json=data)
        response.raise_for_status()
        image_url = response.json()['data'][0]['url']

        with open(image_path, 'wb') as f:
            f.write(requests.get(image_url).content)

        return image_path

    # Listen for "visualize" command
    @commands.command(name='visualize')
    async def visualize(self, ctx, *, text):
        image_path = await self.create_image(text)
        with open(image_path, 'rb') as img_file:
            # Create and send Discord file
            discord_file = discord.File(fp=img_file, filename='visualized_text.png')
            await ctx.send(file=discord_file)

        # Remove the generated image file
        os.remove(image_path)
##implemeted free version of visualize