import discord
from discord.ext import commands
import os
import requests
import json

req = requests.Session()

def checkwhitelist(serverid):
    whitelistpath = "data/client"
    if os.path.isdir(whitelistpath+f"/{serverid}"):
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
    async def on_member_join(self, member):

        server = member.guild
        memberid = member.id
        membername = member.name
        memberdiscrim = member.discriminator

        

        if checkwhitelist(server.id) == True:
            path = f"data/client/{server.id}"
            memberpath = path+f"/user/{memberid}.json"

            with open(path+"/serverformat.json") as f:
                jsondata = json.load(f)
                f.close()
            
            joinlimit = jsondata["joinlimit"]
            joinlog = jsondata["logchannel"]["joinleave"]

            serverpunishlog = jsondata["logchannel"]["serverpunish"]

            spunishmethod = jsondata["serverpunish"]["method"]

            whitelist = jsondata["whitelist"]
            
            #Gets verified datas
            r = req.get(f"http://127.0.0.1:8000/verifydb/{memberid}")
            if r.text == "0":
                verified = "0"
                robloxname = "None"
            else:
                verified = r.text

                r = req.get(f"https://api.roblox.com/users/{verified}").json()
                robloxname = r["Username"]
            
            

            #edits count
            if memberid not in whitelist:

                

                if os.path.isfile(memberpath):
                    with open(memberpath) as f:
                        jsondata = json.load(f)
                        f.close()

                    currentcount = jsondata["join"]
                    currentcount += 1
                    jsondata["join"] = currentcount

                    with open(memberpath, "w") as f:
                        json.dump(jsondata, f, indent=2)
                        f.close()

                else:
                    with open("data/format/userformat.json") as f:
                        jsondata = json.load(f)
                        f.close()

                    jsondata["userid"] = memberid
                    jsondata["join"] = 1

                    currentcount = 1
                    
                    with open(memberpath, "w") as f:
                        json.dump(jsondata, f, indent=2)
                
               
                
            else:
                currentcount = "❌"

            #Send join-log to channel
            if joinlog != 0:
                join = discord.utils.get(self.client.get_all_channels(), id = int(joinlog))

                embed = discord.Embed(
                    title = f"유저가 서버에 들어왔습니다",
                    color = discord.Color.from_rgb(0, 255, 0)
                )
                embed.add_field(name="유저", value=f"{membername}#{memberdiscrim}", inline=False)
                embed.add_field(name="로블이름", value=robloxname, inline=True)
                embed.add_field(name="로블아이디", value=verified, inline=True)
                embed.add_field(name="들어온 횟수", value=currentcount, inline=True)
                embed.set_footer(text="NastyCore, The Next Innovation")

                try:
                    await join.send(embed=embed)
                except:
                    pass
            
            if memberid not in whitelist and joinlimit != 0 and joinlimit != 1:
                if currentcount < joinlimit:
                    pass
                else:
                    #Gets the log channel for punishment
                    
                    if serverpunishlog != 0:
                        spunishlog = discord.utils.get(self.client.get_all_channels(), id = int(serverpunishlog))

                    #Takes action
                    if spunishmethod == 0:
                        pass
                    elif spunishmethod == 1:
                        await member.kick()

                        try:
                            embed = discord.Embed(
                                title = f"서버킥 | {membername}#{memberdiscrim}",
                                description = f"서버에 들어온 횟수: {currentcount}\n킥 하였습니다.",
                                color = discord.Color.from_rgb(255, 255, 0)
                            )
                            embed.set_footer(text="NastyCore, The Next Innovation")
                            embed.set_footer(text="NastyCore, The Next Innovation")
                            await spunishlog.send(embed=embed)
                        except:
                            pass

                    elif spunishmethod == 2:
                        await member.ban()

                        try:
                            embed = discord.Embed(
                                title = f"서버차단 | {membername}#{memberdiscrim}",
                                description = f"서버에 들어온 횟수: {currentcount}\n차단 하였습니다.",
                                color = discord.Color.from_rgb(255, 255, 0)
                            )
                            embed.set_footer(text="NastyCore, The Next Innovation")
                            embed.set_footer(text="NastyCore, The Next Innovation")
                            await spunishlog.send(embed=embed)
                        except:
                            pass

                    else:
                        pass
        else:
            print("not whitelisted.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print("We're sorry to see you go!")

def setup(client):
    client.add_cog(trackuser(client))