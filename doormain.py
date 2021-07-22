import discord
import os
import json
import requests
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True
intents.guilds = True

client = commands.Bot(command_prefix = "-", intents=intents)
client.remove_command('help')


for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

@client.command()
async def load(ctx, name):
    client.load_extension(f"cogs.{name}")
    await ctx.send("Done!")

@client.command()
async def unload(ctx, name):
    client.unload_extension(f"cogs.{name}")
    await ctx.send("Done!")




client.run("ODY3MjA0MTUwNjkzNTkzMTQ4.YPdszQ.cNl8O0sqN4onYZDTRFNHN2SAYK0")