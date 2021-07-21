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
        guildownerid = guild.owner_id
        guildname = guild.name

        guildowner = await guild.fetch_member(guildownerid)

        if checkwhitelist(guildid) == True:
            embed = discord.Embed(
                title = f"성공 | 봇 추가 완료({guildname})",
                description = f"안녕하세요! 도어맨을 구매해주셔서 진심으로 감사합니다. **서버**에서 `-도움말` 명령어를 통해 저를 더 알아가 볼까요?",
                color = discord.Color.from_rgb(0, 255, 0)
            )
            await guildowner.send(embed=embed)
        else:
            embed = discord.Embed(
                title = f"에러 | 화이트리스트가 되지 않은 서버({guildname})",
                description = f"본 서버는 도어맨을 구매한 기록이 없는 것으로 보입니다. 봇을 우선적으로 구매해주세요.\n저는 이만 서버를 나가겠습니다! 추후에 다시 초대해주세요!",
                color = discord.Color.from_rgb(255, 255, 0)
            )
            await guildowner.send(embed=embed)

            await guild.leave()



def setup(client):
    client.add_cog(trackuser(client))