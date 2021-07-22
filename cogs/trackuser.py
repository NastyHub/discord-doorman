import discord
from discord.ext import commands
import os
import requests
import json

req = requests.Session()

mycookie = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_D8A98EF3D11D776EFEB954D8E2896629982ED2B813D55AE6AE438ECE1BA1F622A22B0FECE15437A59194630E9F74A79AE1F9CD898DC03BA2143EC35FF840E956BE2FC1E45442BE0B0CA02E282F00E7CAC53B46F5A62F279E02F3DAF9A184A3BBE7FFFA27B599590DD6DF0136F5C378B61BE0C9511BD5CFCAA430655F88312FA37805E72B99A8EC64045AAD223A79E67CBDB374D8A4B86ABA4FF6085260FC9AB456926F1080B1777416E727C8351FB783EFD73BD0E692533161D6165AC28AC87316AF38083DE6CCE4983E8AC32F9203F22948214B7B8A2864D8CBDB2C7EDC355D9FA5EEA16706C6A5B3CFD8983FB5A99D533DA0419111CD192084415870E86FC23B96BF3CDA7457F7C4F2CECE59217F6B01F66399E71486022AD2995DCEF0174612D60888A60D2947C0E4DEDE97EA11B0F5952544CCC43FE712172ABEC85301F3F0D9AF7A91FB0E00D0776C2900691793FBE429955B95E3A078BC61CE6891666AD188ABCB"
req = requests.Session()
req.cookies[".ROBLOSECURITY"] = mycookie

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
                            await member.send(embed=embed)
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
                            await member.send(embed=embed)
                        except:
                            pass

                    else:
                        pass


    @commands.Cog.listener()
    async def on_member_remove(self, member):
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
            joinlog = jsondata["logchannel"]["joinleave"]
            groupid = jsondata["groupid"]
            grouppunishlog = jsondata["logchannel"]["grouppunish"]
            gpunishmethod = jsondata["grouppunish"]["method"]
            demoterank = jsondata["grouppunish"]["demoterank"]
            whitelist = jsondata["whitelist"]

            if joinlog != 0:
                join = discord.utils.get(self.client.get_all_channels(), id = int(joinlog))

                embed = discord.Embed(
                    title = f"유저가 서버를 퇴장하였습니다",
                    color = discord.Color.from_rgb(255, 255, 0)
                )
                embed.add_field(name="유저", value=f"{membername}#{memberdiscrim}", inline=False)
                embed.set_footer(text="NastyCore, The Next Innovation")

                try:
                    await join.send(embed=embed)
                except:
                    pass

            if memberid not in whitelist:
            
                #Gets verified datas
                r = req.get(f"http://127.0.0.1:8000/verifydb/{memberid}")
                if r.text != "0":
                    verified = r.text
                
                    r = req.get(f"https://api.roblox.com/users/{verified}").json()

                    robloxname = r["Username"]

                    if grouppunishlog != 0 and gpunishmethod != 0 and groupid != 0:
                        punishlog = discord.utils.get(self.client.get_all_channels(), id = int(grouppunishlog))
                        
                        if gpunishmethod == 1:
                            #demotes
                            print("demotes")
                        else:
                            print("kicks.")


                    


def setup(client):
    client.add_cog(trackuser(client))