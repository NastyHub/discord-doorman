import discord
import os
from discord.ext import commands
import json

ownerid = 631441731350691850

formatpath = {
    "client" : "clientformat.json",
    "server" : "serverformat.json",
    "user" : "userformat.json"
}

def checkowner(userid):
    if userid == ownerid:
        return True
    else:
        return False

class owner(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def forceset(self, ctx, serverid, ownerid):
        serverpath = "data/client/" + f"{serverid}"
        if checkowner(ctx.author.id) == True:
            if os.path.isfile(serverpath):
                embed = discord.Embed(
                    title = f"에러 | 이미 구매한 서버",
                    description = f"해당 서버는 도어맨을 구매하였습니다.",
                    color = discord.Color.from_rgb(255, 255, 0)
                )
                await ctx.send(embed=embed)
            else:
                os.mkdir(serverpath)
                os.mkdir(serverpath + "/user")
                
                #CopyPasta clientformat
                with open("data/format/clientformat.json") as f:
                    jsondata = json.load(f)
                    f.close()
                jsondata["purchasemethod"]["method"] = 3
                jsondata["serverid"] = serverid
                jsondata["purchasediscordid"] = ownerid,
                jsondata["purchaserobloxid"] = 0

                with open(serverpath+"/clientformat.json", "w") as f:
                    json.dump(jsondata, f, indent=2)
                    f.close()
                
                #CopyPasta serverformat
                with open("data/format/serverformat.json") as f:
                    jsondata = json.load(f)
                    f.close()
                jsondata["serverid"] = serverid
                jsondata["ownerid"] = ownerid
 
                with open(serverpath+"/serverformat.json", "w") as f:
                    json.dump(jsondata, f, indent=2)
                    f.close()

                embed = discord.Embed(
                    title = f"성공 | 수동 화이트리스트",
                    description = f"해당 서버를 수동으로 화이트리스팅 했습니다.",
                    color = discord.Color.from_rgb(0, 255, 0)
                )
                await ctx.send(embed=embed)

        else:
            await ctx.send("no.")

def setup(client):
    client.add_cog(owner(client))