# Travis Hawks
# This Discord Bot is a learning project and is used to help administrate a Discord server with 500+ members.
# Currently hosted and live on Amazon Free tier AWS 24/7.

# Potential upgrades / fixes / idea's
# look into better string concatination. string + string is the inneficient method. 
# xerics guide / attacks. just like the ?<tag> thing in discord.py
# tob guide / attacks. 
# boss gp/h - requires scrapping.
# update help/info

import discord
import asyncio
import Splitrecord
import random
import datetime
from datetime import timedelta
from discord.ext import commands

# global fields
token = 'NDY3MjA0NDkwODk1MDMyMzIw.DisQvw.PTOmql6rY-_I04z1gq5a0Cp_Wds'
bot = commands.Bot(command_prefix='./')
bot.remove_command("help")
dict = {}
splitlog = {}
server = None
inactiverole = None
events = []

trialmembers = {} #outdated
adminroles = [] # outdated

@bot.event
async def on_ready():
    global server
    global adminroles
    for x in bot.servers:
        if x.name.lower() == "logical pvm":
            server = x
            break
    for x in server.roles:
        if x.name.lower() == "inactive":
            inactiverole = x
            break
        
    loaddict()
    loadsplitlog()
    loadtrialmembers()
    print('Bot is ready for use')

# info / help COMMAND.
# provides information on Discord Bot use for Discord members.
# UPDATE on every change / new COMMAND added.
@bot.command(pass_context=True, name = "info", aliases = ["help"])
async def info(ctx):
    embed = discord.Embed(title="HawkBot", description="Prototype bot, V1.3.", color=0x29E812)

    embed.add_field(name="Author", value="Hawk0742 (Thawks)")
    embed.add_field(name="Bot prefix", value= "Bot prefix is ""./""")
    embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

    embed.add_field(name="Common commands", value= "Press 1 to view a list of common NON STAFF commands.")
    embed.add_field(name="Event commands", value= "Press 2 to view a list of event commands.")
    embed.add_field(name="Admin commands - splits", value= "Press 3 to view a list of admin split related commands.")
    embed.add_field(name="Admin Commands - trialMembers", value= "Press 4 to view a list of trial member related commands.")
    embed.add_field(name="Admin commands2", value= "Press 5 for higher admin commands. These are probably only for Bae Hawk.")

    await bot.say(embed=embed)
    embed = discord.Embed(title="HawkBot", description="Prototype bot, V1.3.", color=0x29E812)
    await bot.say("Please press 1, 2, 3, 4, or 5 to get to the correct interface! Read above embed for help.")
    msg = await bot.wait_for_message(author=ctx.message.author)

    if msg.content == "1":
        embed.add_field(name="checksplt", value="Returns the amount of saved splits in persons name.  " +
                    "USAGE: <prefix>checksplit <username>   EXAMPLE: ./checksplit @hawk0742 (thawks)")
        embed.add_field(name="osrsmeme", value="Returns a osrs meme! " +
                    "USAGE: <prefix>osrsmeme   EXAMPLE: ./osrsmeme")
        embed.add_field(name="bosstask", value="Returns a random boss task! Includes GWD, raids, wildy bosses, and more. " +
                    "USAGE: <prefix>bosstask   EXAMPLE: ./bosstask")
    
    elif msg.content == "2":
        embed.add_field(name="addevent", value=" Prompts user to input event information and makes an embed.  " + 
                    "USAGE: <prefix>addevent   EXAMPLE: ./addevent")
        embed.add_field(name="removeevent", value="Asks user if the first / oldest event should be deleted, then deletes it.   " +
                    "USAGE: <prefix>removeevent    EXAMPLE: ./removeevent")
        embed.add_field(name="listevents", value="Lists all saved events as embeds.   " + 
                    "USAGE: <prefix>listevents   EXAMPLE: ./listevents")
        embed.add_field(name="pingevent", value="pings everyone with the first / oldest event embed.   " +
                    "USAGE: <prefix>pingevent   EXAMPLE: ./pingevent")

    elif msg.content == "3":
        embed.add_field(name="addsplit", value="Adds/subtracts GP amount to users saved splits. REQUIRES: Admin.  " +
                    "USAGE: <prefix>addsplit <username> <gpAmount>    EXAMPLE: ./addsplit @hawk0742 500000")
        
        embed.add_field(name="checksplt", value="Returns the amount of saved splits in persons name.  " +
                    "USAGE: <prefix>checksplit <username>   EXAMPLE: ./checksplit @hawk0742 (thawks)")
    
    elif msg.content == "4":
        embed.add_field(name="addtrialmember", value="adds a member and their join date to list. REQUIRES: staff role.  USAGE: " +
                    " <prefix>addtrialmember <username>   EXAMPLE: ./addtrialmember @hawk0742")
        
        embed.add_field(name="removetrialmember", value="removes a member and their join date to list. REQUIRES: staff role.  USAGE: " +
                    " <prefix>removetrialmember <username>   EXAMPLE: ./removetrialmember @hawk0742")
        embed.add_field(name="gettrialmember", value="returns a member and their join date. REQUIRES: staff role.  USAGE: " +
                    " <prefix>gettrialmember <username>   EXAMPLE: ./gettrialmember @hawk0742")
        embed.add_field(name="listtrialmembers", value="returns an embeded message with all trialmembers. REQUIRES: staff role.  USAGE: " +
                    " <prefix>liattrialmembera   EXAMPLE: ./listtrialmember")

    elif msg.content == "5":
        embed.add_field(name="savedict", value="saves current dict values to txt file.")
        embed.add_field(name="savesplitlog", value="saves the splitlog manually. REQUIRES: staff role.  USAGE: " +
                    " <prefix>savesplitlog     EXAMPLE: ./savesplitlog")
        embed.add_field(name="markinactives", value="manually calls for marking of inactives. inactive time preset to 1 month. " + 
                    "REQUIRES: staff role.  USAGE: <prefix>markinactives    EXAMPLE: ./markinactives")
        embed.add_field(name="setadminroles", value="Adds/Removes a rank from staff list. REQUIRES: admin(ownership).  " +
                    "USAGE: <prefix>setadminroles <add/remove> <role>   EXAMPLE: ./setadminroles remove @captain")
        embed.add_field(name="setinactiverole", value="sets the servers inactive role. Used for marking inactive users. REQUIRES: " +
                    " staff role.  USAGE: <prefix>setinactiverole <role>    EXAMPLE: ./setinactiverole @INACTIVE")
        embed.add_field(name="setserver", value="sets the server id. REQUIRES: admin(ownership)   USAGE: <prefix>setserver  " +
                    "  EXAMPLE: ./setserver")

    else:
        await bot.say("Whatever you typed I didnt understand! Please try again.")

    await bot.say(embed=embed)


# COMMAND to update the current currency splitcount for a given member
# adds gp/ split count to a a specified member.
@bot.command(pass_context=True, name='addsplit', aliases=['Addsplit', "add split"])
@commands.has_permissions(manage_server=True)
async def addsplit(ctx, member: discord.Member, message):
    msg2 = await bot.say("Are you sure you want to update " + member.display_name + "'s split count by: " + format(int(message), ',d') + "? Please " +
                  "respond with \"yes\" or \"no\".")

    msg = await bot.wait_for_message(author=ctx.message.author)
    if msg.content.lower().startswith("yes"):
        if member.name in splitlog:
                splitlog[member.name] = Splitrecord.Splitrecord(member.name, int(message) +
                            int(splitlog.get(member.name).splitcount), ctx.message.timestamp.strftime("%Y-%m-%d %H:%M:%S"))

        else:
                splitlog[member.name] = Splitrecord.Splitrecord(member.name, int(message),
                            ctx.message.timestamp.strftime("%Y-%m-%d %H:%M:%S"))

        await bot.say("Record updated. " + member.display_name + " split total is now " +
                    format(splitlog.get(member.name).splitcount, ',d') + ". Added value was: " + format(int(message), ',d') + 
                    ". Updated on: " + ctx.message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    + " by " + ctx.message.author.display_name + ". ")
        
        savesplitlog2()
        

    elif msg.content.lower().startswith("no"):
        await bot.say("SplitCount for " + member.display_name + " NOT updated.")

    else:
        await bot.say("Error... Splitcount for " + member.display_name + " NOT updated. I dont think you said \"yes\" or \"no\"")
            
    await bot.delete_messages([ctx.message, msg, msg2])


# COMMAND to check the current splitcount of a given member
@bot.command(pass_context=True)
async def checksplit(ctx, member: discord.Member):
    try:
        await bot.say("Member " + member.display_name + " has: " + format(int(splitlog.get(member.name).splitcount), ',d') + "GP in splits.")
    except AttributeError:
        await bot.say(member.display_name + " has no recorded splits at this time.")

    await bot.delete_message(ctx.message)



# COMMAND. savedict method. saves all entries (discord members) in dict into a .txt file for later re-use / loading on restart.
@bot.command(pass_context=True)
@commands.has_permissions(manage_server=True)
async def savedict(ctx):
    file = open(server.name + 'ActivityLog.txt', 'w')
    try:
        for x in dict:
            file.write(str(x) + ", " + dict.get(x) + "\n")
    except UnicodeEncodeError:
        pass
        
    file.close()
    await bot.say("Dictionary was saved.")



# loaddict method. loads old entries from file into dict. currently is automatically called on bot restart.
def loaddict():
    file = open(server.name + 'ActivityLog.txt', 'r')
    try:
        for line in file:
            if line == "\n":
                continue
            vector = line.split(",")
            dict[vector[0]] = vector[1]
        print("loaded dict file just fine")
    
    except FileNotFoundError:
        print("failed to load dict file.")
        # at this time I cant get this to work.  apparently I cant make a member. will ask for help later
        # await bot.send_message(thawks, "I failed to load dic file.")
    file.close()


# COMMAND. savesplitlog method. saves all entries in dict into a .txt file.
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def savesplitlog(ctx):
    file = open(server.name + 'Splitlog.txt', 'w')
    for x in splitlog:
        try:
            file.write(str(x) + "," + str(splitlog.get(x).splitcount) + "," + splitlog.get(x).lastupdate +"\n")
        except AttributeError:
            print("ok error...")
            print(x + "   " + str(splitlog.get(x)))
    file.close()
    await bot.say("Splitlog was saved.")


# COMMAND. saves the list of trial members into a .txt file.
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def savetrialmembers(ctx):
    file = open(server.name + 'Trialmembers.txt', 'w')
    for x in trialmembers:
        file.write(str(x) + ", " + str(trialmembers.get(x)) +"\n")
    file.close()
    await bot.say("Trialmembers were saved.")



# loadsplitlog method. loads old entries from file into dict. currently is automatically called on bot restart.
def loadsplitlog():
    try:
        file = open(server.name + 'Splitlog.txt', 'r')
        for line in file:
            if line == "\n":
                continue
        
            vector = line.split(",")
            splitlog[vector[0]] = Splitrecord.Splitrecord(vector[0].strip(), vector[1].strip(), vector[2].strip())
        file.close()
        print("loaded splitlog file just fine")
    except FileNotFoundError:
        print("failed to load splitlog file.")


# COMMAND. Marks all inactive discord accounts within the server as Global inactiverank role in discord.
# Used to help manage inactive accounts.
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def markinactives(ctx):
    month = datetime.datetime.today().strftime("%m")
    day = datetime.datetime.today().strftime("%d")
    global server
    global inactiverole
    if inactiverole == None:
        inactiverole = server.roles[1] # sets inactiverole to 1 above @everyone by default.
    for x in dict:
        if int(month)-int(dict.get(x)[5:7]) >=0 and int(day) >= int(dict.get(x)[8:10]):
             # give inactive tag
            await bot.add_roles(server.get_member(x[x.find("::")+2:]), inactiverole)
             # await bot.add_roles
    await bot.send_message(ctx.message.channel, "markinactives command completed run.")

#COMMAND. Adds a discord member as a trialmember in the trialmember dict.
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def addtrialmember(ctx, member: discord.Member):
    trialmembers[member.name + "::" + str(member.id)] = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    await bot.say(member.display_name + " has been added as a trial member.")
    await bot.send_message(member, "You have been accepted into Logical Pvm as a trial member! Welcome to the clan. " +
            "Trial membership lasts for 2 weeks. During that time you can do everything a full member can while also working " +
            " on completing the full clan requirements. After 2 weeks you will either be promoted to a full member if you " +
            " finished requirements or you will be demoted. Should you be demoted, you will need to finish requirements / re-apply. " +
            " If you have any questions, please contact a staff member (gold stars)." + 
            " Best of luck!")

    savetrialmembers2()


# COMMAND. removes a given discord member from the list of trialmembers.
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def removetrialmember(ctx, member: discord.Member):
    if trialmembers.__contains__(member.name + "::" + member.id):
        trialmembers.pop(member.name + "::" + member.id)
        await bot.say(member.display_name + " has been removed from trialmembers.")
        savetrialmembers2()
    
    else:
        await bot.say(member.display_name +  " is/was not listed as a trial member.")


# COMMAND. sends an embed in discord with the list of current trialmembers. 
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def listtrialmembers(ctx):
    embed = discord.Embed(title="Trial members list.", description="List of current trial members. name and join date.", color=0x29E812)
    for x in trialmembers:
        embed.add_field(name=server.get_member(x[x.find("::")+2:]), value= trialmembers.get(x)) 
    await bot.say(embed=embed)


# COMMAND. returns the trial information about a trialmember or reports that the discord members is not a trialmember.
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def gettrialmember(ctx, member: discord.Member):
    if member.name + "::" + member.id in trialmembers:
        await bot.say(member.display_name + "  joined: " + trialmembers.get(member.name + "::" + member.id))
        
    else:
        await bot.say(member.display_name + " is not listed as a trial member.")


# COMMAND. Fun command to randomly assign a discord member a "Boss task".
@bot.command(pass_context=True)
async def bosstask(ctx):
    # dups to add weighting
    gwd = ["Graardor", "Zilyana", "Kril", "Kree'arra", "Graardor"]
    wildy = ["Callisto", "Venenatis", "Chaos Elemental", "Scorpia", "Crazy Archaeologist", "Chaos Fanatic", "Vet'ion"]
    demiBoss = ["KBD", "Kalphite Queen", "Mole"]
    other = ["Zulrah", "Vorkath"]
    bosses = ["gwd", "gwd", "gwd", "wildy", "demiboss", "other", "other"]
    
    index = random.randint(0,6)
    if bosses[index] == "gwd":
        index = random.randint(0, len(gwd)-1)
        amount = random.randint(5,20)
        await bot.say("You have been assigned to kill " + gwd[index] + " " + str(amount)+ " times. GL!")
    elif bosses[index] == "wildy":
        index = random.randint(0, len(wildy)-1)
        amount = random.randint(1,5)
        await bot.say("You have been assigned to kill " + wildy[index] + " " + str(amount) + " times. GL!")
    elif bosses[index] == "demiboss":
        index = random.randint(0, len(demiBoss)-1)
        amount = random.randint(10,30)
        await bot.say("You have been assigned to kill " + demiBoss[index] + " " + str(amount) + " times. GL!")
    elif bosses[index] == "other":
        index = random.randint(0, len(other)-1)
        amount = random.randint(10,30)
        await bot.say("You have been assigned to kill " + other[index] + " " + str(amount) + " times. GL!")
    else:
        await bot.say("Woops. Error. Please tell hawk.")


# COMMAND. A fun command to give a member a saved joke about Old Scholl Runescape. 
@bot.command(pass_context=True)
async def osrsmeme(ctx):
    number = random.randint(1,14)
    myfile = open("C:/Users/Administrator/Desktop/Discord Bot1/" + str(number) + ".jpg", 'rb')
    await bot.send_file(ctx.message.channel, myfile)
    myfile.close()

# COMMAND. Creates a discord embed regarding an upcoming event for the members. Embed is saved.
@bot.command(pass_context=True)
# @commands.has_permissions(manage_server=True)
async def addevent(ctx):

    for item in ctx.message.author.roles:
        if item.name == "Event Helper" or item.name == "Admin":
            
            title = day = time = description = rules = people = ""
            await bot.say("Event title?")
            title = await bot.wait_for_message(20, author=ctx.message.author)
            title = title.content
            await bot.say("Event day?")
            day = await bot.wait_for_message(20, author=ctx.message.author)
            day = day.content
            await bot.say("Event time?")
            time = await bot.wait_for_message(20, author = ctx.message.author)
            time = time.content
            await bot.say("Event description?")
            description = await bot.wait_for_message(20, author = ctx.message.author)
            description = description.content
            await bot.say("Event Rules?")
            rules = await bot.wait_for_message(20, author = ctx.message.author)
            rules = rules.content
            await bot.say("Assigned Staff / Event Cordinators?")
            people = await bot.wait_for_message(20, author = ctx.message.author)
            people = "Assigned staff: " + people.content
            await bot.say("Creating event.")

            embed = discord.Embed(title=title, description="Clan Event!" , color=0x20E400)
            embed.add_field(name="day", value= day)
            embed.add_field(name="time", value= time)
            embed.add_field(name = "description", value = description)
            embed.add_field(name = "rules", value = rules)
            embed.set_footer(text = people) 
            await bot.say(embed=embed)
            events.append(embed)
            break


# COMMAND. Removes the first embed in the list of saved event embeds.
@bot.command(pass_context=True)
# @commands.has_permissions(manage_server=True)
async def removeevent(ctx):
    x = ""
    for s in server.roles:
        if (s.name  == "Event Helper" or s.name == "Admin"):
            x = s
            break
    if (x in ctx.message.author.roles):
        await bot.say("Remove this event?", embed = events[0])
        msg = await bot.wait_for_message(author = ctx.message.author)
        if msg.content.lower().startswith("yes"):
            events.pop(0)
            await bot.say("Event removed.")
        elif msg.content.lower().startswith("no"):
            await bot.say("Event NOT removed.")
        else:
            await bot.say("Your input didnt match what I wanted. Please try again.")


# COMMAND. Sends out a discord ping to @everyone when called to alert members of a new event.
@bot.command(pass_context=True)
# @commands.has_permissions(manage_server=True)
async def pingevent(ctx):
    x = ""
    for s in server.roles:
        if (s.name  == "Event Helper" or s.name == "Admin"):
            x = s
            break
    if (x in ctx.message.author.roles):
        await bot.delete_message(ctx.message)
        await bot.say("@everyone, Our upcoming event!", embed = events[0])


# COMMAND. Lists the current saved event embeds.
@bot.command(pass_context=True)
async def listevents(ctx):
    for x in events:
        await bot.say(embed = x)

# COMMAND. gives the author the discord tag requested. Currently only a few tags are supported to prevent tag abuse.
@bot.command(pass_context=True)
async def givetag(ctx, message, *rest):
    for part in rest:
        message += " " + part

    s = ""
    for x in server.roles:
        if message == x.name:
            s = x
    if (message == "TOB"):
        await bot.add_roles(ctx.message.author, s)
    
    elif(message == "Raids1"):
        await bot.add_roles(ctx.message.author, s)
    
    elif(message == "looking for raids team"):
        await bot.add_roles(ctx.message.author, s)

    elif(message == "Admin"):
        await bot.say("you cannot give yourself Admin. Hawk has been alerted.")
        return

    else:
        await bot.say("I dont think thats a valid role or its a role you cant assign to yourself. You can assign " +
                    "these roles: TOB, Raids1, looking for raids team")
        await bot.delete_message(ctx.message)
        await bot.say(message)
        return

    await bot.delete_message(ctx.message)
    await bot.say("Your role as been added.")


# COMMAND. Removes a tag once a member no longer wants that tag.
@bot.command(pass_context=True)
async def removetag(ctx, message, *rest):
    for part in rest:
        message += " " + part
        
    s = ""
    for x in server.roles:
        if message == x.name:
            s = x
    if (message == "TOB"):
        await bot.remove_roles(ctx.message.author, s)
    
    elif(message == "Raids1"):
        await bot.remove_roles(ctx.message.author, s)
    
    elif(message == "looking for raids team"):
        await bot.remove_roles(ctx.message.author, s)

    else:
        await bot.say("I dont think thats a valid role or its a role you cant remove from yourself. You can remove " +
                    "these roles: TOB, Raids1, looking for raids team")
        await bot.delete_message(ctx.message)
        return

    await bot.delete_message(ctx.message)
    await bot.say("Your role as been removed.")



def savetrialmembers2():
    file = open(server.name + 'TrialMembers.txt', 'w')
    for x in trialmembers:
        file.write(str(x) + ", " + trialmembers.get(x)+"\n")
    file.close()


def loadtrialmembers():
    file = open(server.name + 'TrialMembers.txt', 'r')
    try:
        for line in file:
            if line == "\n":
                continue
            vector = line.split(",")
            trialmembers[vector[0]] = vector[1].strip()
        print("loaded trialmembers file just fine")
    except FileNotFoundError:
        print("failed to load trialmembers file.")
        
    file.close()


# on every message this runs. current use: reads a post and gets author, updates authors last post for activity
@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        dict[str(message.author) + "::" + str(message.author.id)] = message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
       


def savedict2():
    file = open(server.name + 'ActivityLog.txt', 'w')
    try:
        for x in dict:
            file.write(str(x) + ", " + dict.get(x) + "\n")
    except UnicodeEncodeError:
        pass
        # continue  : wrong placement apprently
    file.close()
    # await bot.say("Dictionary was saved.")


def savesplitlog2():
    file = open(server.name + 'Splitlog.txt', 'w')
    for x in splitlog:
        try:
            file.write(str(x) + ", " + str(splitlog.get(x).splitcount) + ", " + splitlog.get(x).lastupdate + "\n")
        except AttributeError:
            print(x + "  " + str(splitlog.get(x)))
        except UnicodeEncodeError:
            print("~~~~UnicodeEncodeError!!~~~~~")
            print("  " + splitlog.get(x).username + "   kok")
            del splitlog[x]
            
    file.close()



async def markinactives2():
    month = datetime.datetime.today().strftime("%m")
    day = datetime.datetime.today().strftime("%d")
    global server
    global inactiverole
    for x in dict:
        if int(month)-int(dict.get(x)[5:7]) >=0 and int(day) >= int(dict.get(x)[8:10]):
            # give inactive tag
            await bot.add_roles(server.get_member(x[x.find("::")+2:]), inactiverole)
            # await bot.add_roles


@bot.listen()
async def on_member_remove(member: discord.Member):
    welcome_channel = ""
    for x in server.channels:
        if x.name == "welcome":
            welcome_channel = x
    if member.display_name in splitlog:
        await bot.send_message(welcome_channel, "Buh Bye " + member.display_name + ". You left with: " +
        splitlog.get(member.name).splitcount + "  in recorded splits.")
        splitlog.pop(member)
    else:
        await bot.send_message(welcome_channel, "Buh Bye " + member.display_name +
                               " you left with no recorded splits.")
    dict.pop(str(message.author) + "::" + str(message.author.id))
    trialmembers.pop(member)


@bot.listen()
async def on_member_join(member: discord.Member):
    welcome_channel = ""
    for x in server.channels:
        if x.name == "welcome":
            welcome_channel = x

    await bot.send_message(welcome_channel, "Hello " + member.display_name + ". welcome to our server. " +
                           "Please post your gearcheck in #gearcheck . If you have questions, please @admin." +
                           " Enjoy PVMing! ")



async def my_background_task():
    await bot.wait_until_ready()
    global server
    
    count = 0
    list = bot.get_all_channels()
    channel = None
    for x in list:
        if x.name == "bots":
            channel = x
    while not bot.is_closed:
        await asyncio.sleep(21600) # task runs every 6 hr / 21600 seconds
        count +=1
        try:
            savesplitlog2()
            savetrialmembers2()
            savedict2()
        except Exception as e:
            print(e)
            raise
        
        print("Saved files this many times: " + str(count))
        await bot.send_message(channel, "Logs are saved.")

        

async def connect():
    print('Logging in...')
    while not bot.is_closed:
        try:
            print('again')
            await bot.start(token)
        except:
            await asyncio.sleep(50)


bot.loop.create_task(my_background_task())
bot.run(token)



