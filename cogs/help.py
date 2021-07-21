import discord
from discord.ext import commands

class help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["도움말"])
    async def help(self, ctx, whattype=None):
        await ctx.send("Still working on it.")

def setup(client):
    client.add_cog(help(client))