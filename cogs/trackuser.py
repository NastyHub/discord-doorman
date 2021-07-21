import discord
from discord.ext import commands

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
        print(f"ID: {self.client.id}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(member.id)
        

def setup(client):
    client.add_cog(trackuser(client))