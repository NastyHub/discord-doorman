import discord
from discord.ext import commands
import os

def checkwhitelist(serverid):
    whitelistpath = "data/client"
    if os.path.isfile(whitelistpath+f"/{serverid}"):
        return True
    else:
        return False

class trackuser(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        printme = '''
        /$$   /$$        /$$$$$$         /$$$$$$        /$$$$$$$$       /$$     /$$
        | $$$ | $$       /$$__  $$       /$$__  $$      |__  $$__/      |  $$   /$$/
        | $$$$| $$      | $$  \ $$      | $$  \__/         | $$          \  $$ /$$/ 
        | $$ $$ $$      | $$$$$$$$      |  $$$$$$          | $$           \  $$$$/  
        | $$  $$$$      | $$__  $$       \____  $$         | $$            \  $$/   
        | $$\  $$$      | $$  | $$       /$$  \ $$         | $$             | $$    
        | $$ \  $$      | $$  | $$      |  $$$$$$/         | $$             | $$    
        |__/  \__/      |__/  |__/       \______/          |__/             |__/    
        '''

        print(printme)

        print("Initializing..")
        print(f"ID: {self.client.user.id}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guildid = guild.id
        guildowner = guild.owner
        guildname = guild.name

        '''
        embed = discord.Embed(
            title = "에러 | 서버 연동된 상태",
            description = f"❗ 현재 이미 {pastgroupid}로 연동된 그룹이 있습니다. 만약 진행하신다면 수동으로 연결했던 모든 역할들이 사라질 겁니다. 계속하시겠습니까?\n'예', '아니요'",
            color = discord.Color.from_rgb(255, 255, 0)
        )
        await ctx.send(embed=embed)
        '''

def setup(client):
    client.add_cog(trackuser(client))