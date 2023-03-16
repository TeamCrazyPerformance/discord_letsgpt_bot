import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello I am Bot!')


bot.run(os.environ['DISCORD_TOKEN'])