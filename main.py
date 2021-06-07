from discord.ext import commands
import asyncio
import random
import time
import requests
import discord.utils
from discord.ext.commands import CommandNotFound
from discord.ext.commands import has_permissions
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions
import aiofiles
import re

import webbrowser

from webserver import keep_alive

import os
from pathlib import Path



intents = discord.Intents.default()
intents.members = True

client = discord.Client()
client = commands.Bot(command_prefix="/", intents=intents)
client.remove_command('help')
client.warnings = {}

counter = 0


# it may throw an error when a member joins when the bot isn't running

Spam = []

channelToSave= []
categoriesToSave= []
VoiceToSave = []

LongoBool = False


@client.event
async def on_ready():

    version = discord.Game(f"/Help | {len(client.guilds)} Guilds | {sum([len(guild.members)for guild in client.guilds])} Members ")
    await client.change_presence(status=discord.Status.online, activity=version)

    for guild in client.guilds:
        client.warnings[guild.id] = {}
        
        async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
            pass

        async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    client.warnings[guild.id][member_id][0] += 1
                    client.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    client.warnings[guild.id][member_id] = [1, [(admin_id, reason)]] 
    
    print(client.user.name + " is ready.")



@client.event
async def on_guild_join(guild):
    client.warnings[guild.id] = {}

    version = discord.Game(f"/Help | {len(client.guilds)} Guilds | {sum([len(guild.members)for guild in client.guilds])} Members ")
    await client.change_presence(status=discord.Status.online, activity=version)

@client.event
async def on_member_join(member: discord.Member=None):
  print ("Ciao")

  version = discord.Game(f"/Help | {len(client.guilds)} Guilds | {sum([len(guild.members)for guild in client.guilds])} Members ")
  await client.change_presence(status=discord.Status.online, activity=version)


@client.event
async def on_member_remove(member: discord.Member=None):
  print ("Addio")

  version = discord.Game(f"/Help | {len(client.guilds)} Guilds | {sum([len(guild.members)for guild in client.guilds])} Members ")
  await client.change_presence(status=discord.Status.online, activity=version)



@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title="**__『MISSING ARGUMENT』__**", description="The argument is missing, add something after the command.", color=0x000000)
        embed.set_image(url="https://img.memecdn.com/when-friends-get-into-an-argument_o_1147117.gif")
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed1=discord.Embed(title="**__『MISSING PERMISSIONS』__**", description="Looks like you're missing the permissions to run this command.", color=0x000000)
        embed1.set_image(url="https://i.nyxbot.xyz/files/articles/permission.gif")
        await ctx.send(embed=embed1)
    if isinstance(error, commands.BotMissingPermissions):
        embed4=discord.Embed(title="**__『BOT MISSING PERMISSIONS』__**", description="I-impossible... The bot is missing permissions...", color=0x000000)
        embed4.set_image(url="https://i.nyxbot.xyz/files/articles/permission.gif")
        await ctx.send(embed=embed4)
    if isinstance(error, CommandNotFound):
      embed=discord.Embed(title="**__『COMMAND NOT FOUND』__**", description="\n```\nOh? Looks like that you executed an unknown command..., you should try using '/Help'\n```\n", color=0x000000)
      embed.set_image(url="https://cdn.dribbble.com/users/183518/screenshots/1766471/agigen-404.gif")
      await ctx.send(embed=embed)
      return
    raise error

@client.command()
@commands.has_permissions(administrator=True)
async def AddID(ctx, ID=None):
  client.warnings[ID] = {}
  print(ID)

@client.command()
async def servers(ctx):
    await ctx.send(f"I am in {len(client.guilds)}")

@client.command()
async def Help(ctx1):
  text = f"""
          **/HelpChannel** ```See the help for the channel```\n
          **/HelpModeration** ```See the help for the channel```\n
          """

  embed=discord.Embed(title=f"COMMANDS\n", description=text, color=0x000000)
  embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
  await ctx1.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members = True)
async def Ban(ctx, user: discord.Member, *, reason = None):
  if not reason:
    await user.ban()
    embed=discord.Embed(title = 'Banned', color=0xe91e63)
    embed.add_field(name = "User was banned", value = f"```**{user}** has been banned for **no reason**.```")
    embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
    await ctx.send(embed=embed)
  else:
    await user.ban(reason=reason)
    embed=discord.Embed(title = 'Banned', color=0xe91e63)
    embed.add_field(name = "User was banned", value = f"```**{user}** has been banned for **{reason}**.```")
    embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members = True)
async def Unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.banned_users

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      embed=discord.Embed(title = 'Unbanned', color=0xe91e63)
      embed.add_field(name = "User was unbanned", value = f"```**{user}** has been ubanned.```")
      embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
      await ctx.send(embed=embed)
      #await ctx.send(f"{user} have been unbanned sucessfully")

@client.command()
@commands.has_permissions(kick_members=True)
async def Kick(ctx, user: discord.Member, *, reason = None):
  if not reason:
    await user.kick()
    embed=discord.Embed(title = 'Kick', color=0xe91e63)
    embed.add_field(name = "User was kikked", value = f"```**{user}** has been kicked for **no reason**.```")
    embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
    await ctx.send(embed=embed)
  else:
    await user.kick(reason=reason)
    embed=discord.Embed(title = 'Kick', color=0xe91e63)
    embed.add_field(name = "User was kikked", value = f"```**{user}** has been kicked for **{reason}**.```")
    embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
    await ctx.send(embed=embed)
    await ctx.send()


@client.command()
@commands.has_permissions(ban_members=True)
async def Warn(ctx, member: discord.Member=None, *, reason=None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
        
    if reason is None:
        return await ctx.send("Please provide a reason for warning this user.")

    try:
        first_warning = False
        client.warnings[ctx.guild.id][member.id][0] += 1
        client.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

    except KeyError:
        first_warning = True
        client.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

    count = client.warnings[ctx.guild.id][member.id][0]

    async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")

    await ctx.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")


@client.command()
@commands.has_permissions(administrator=True)
async def Warnings(ctx, member: discord.Member=None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
    
    embed = discord.Embed(title=f"Displaying Warnings for {member.name}", description="", colour=discord.Colour.red())
    try:
        i = 1
        for admin_id, reason in client.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            embed.description += f"**Warning {i}** given by: {admin.mention} for: *'{reason}'*.\n"
            i += 1

        await ctx.send(embed=embed)

    except KeyError: # no warnings
        await ctx.send("This user has no warnings.")

@client.command()
@commands.has_permissions(ban_members=True)
async def Clearwarnings(ctx, member: discord.Member=None):
    if member is None:
      return await ctx.send("The provided member could not be found or you forgot to provide one.")
    
    embed = discord.Embed(title=f"Displaying Warnings for {member.name}", description="", colour=discord.Colour.red())
    try:
        i = 1
        for admin_id, reason in client.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            client.warnings.pop(admin)
            client.warnings.pop(reason)
            embed.description += f"**Warning {i}** given by: {admin.mention} for: *'{reason}'*.\n"
            i += 1

        await ctx.send(embed=embed)



    except KeyError: # no warnings
      embed2 = discord.Embed(title=f"The warnings of {member.name} were remove", description="", colour=discord.Colour.red())
      await ctx.send(embed2=embed2)

    for guild in client.guilds:
        client.warnings[guild.id] = {}
        
        async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
            pass

        async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    client.warnings[guild.id][member_id][0] += 1
                    client.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    client.warnings[guild.id][member_id] = [1, [(admin_id, reason)]] 

@client.command()
@commands.has_permissions(manage_channels=True, administrator=True)
async def Purge(ctx3, repeat=0):

  try:

    await ctx3.channel.purge(limit=repeat) 

  
    embed = discord.Embed(title=f"The message were delete", description="", colour=discord.Colour.green())
    await asyncio.sleep(2)
    await ctx3.send(embed=embed)

  except  ValueError:
    embed3 = discord.Embed(title=f"{repeat} isn't a number", description="", colour=discord.Colour.red())
    await ctx3.send(embed3=embed3)

  else:
    embed4 = discord.Embed(title=f"{repeat} isn't a number", description="", colour=discord.Colour.red())
    await ctx3.send(embed4=embed4)

  finally:
    embed4 = discord.Embed(title=f"{repeat} isn't a number", description="", colour=discord.Colour.red())
    await ctx3.send(embed4=embed4)

@client.command()
async def Report(ctx, linkDelmsg):
  embed=discord.Embed(title=f"REPORT from {ctx.author} \n", description=f"```Here is a report:```\n {linkDelmsg}", color=0x000000)
  embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
  ownerr = ctx.guild.owner

  await ownerr.send(embed=embed)

  embed=discord.Embed(title=f"REPORT COMPLETE\n", description=f"```The report is completed\n```", color=0x000000)
  embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")

  await ctx.send(embed=embed)


@client.command()
async def HelpChannel(ctx2):
  text = f"""
          **/SaveChannel**```for saving the text channels```\n
          **/SaveVoiceChannel**```for saving the voice channels```\n
          **/SaveCategories**```for saving the categories```\
          
          **/Restore**```+ the backup code of the text channels```\n
          **/RestoreVoiceChannel**```+ the backup code of the voice channels```\n
          **/RestoreCategories**```+ the backup code of the categories```\n
          **/BackupList**\n```For see your backup codes```
          """


  embed=discord.Embed(title=f"COMMANDS FOR THE THE CHANNEL\n", description=text, color=0x000000)
  embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")

  await ctx2.send(embed=embed)

@client.command()
async def HelpModeration(ctx1):
  text = f"""
          **/Ban**```+ the user that you want to ban```\n
          **/Kick**```+ the user that you want to kick```\n
          **/Warn**```+ the member that you want to warn```\n
          **/Warnings**```+ the member for see his/her warnings```\n
          **/ClearWarnings**```+ the member for clear his/her warnings```\n
          **/Purge**```+ the number of the message that you want to delete```\n
          **/Report**```+ link of the message that you want to report (it sends it privat to the owner)```\n
          """


  embed=discord.Embed(title=f"COMMANDS FOR THE THE MODERARION\n", description=text, color=0x000000)
  embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")

  await ctx1.send(embed=embed)

@client.command()
@commands.has_permissions(manage_channels=True, administrator=True)
async def SaveChannel(ctx3):

  random_string = ''

  for _ in range(10):
     # Considering only upper and lowercase letters
      random_integer = random.randint(97, 97 + 26 - 1)
      flip_bit = random.randint(0, 1)
    # Convert to lowercase if the flip bit is on
      random_integer = random_integer - 32 if flip_bit == 1 else random_integer
    # Keep appending random characters using chr(x)
      random_string += (chr(random_integer))


  for channel in ctx3.guild.channels:
    if channel.type == discord.ChannelType.text:
      VoiceToSave.append(channel)
  
      with open(random_string, "w") as f:
        for s in VoiceToSave :
          f.write(str(s) +"\n")

        #await asyncio.sleep(500)
        #random_string = ""

    else:
      pass
  
    
  with open (str(ctx3.author.id), "a")  as list:
    list.write(f"{ctx3.guild.name} {random_string} text channels\n")

  print(random_string)

  embed=discord.Embed(title = 'The text channels were save!', color=0x000000)
  embed.add_field(name = "/Restore +", value = random_string)
  embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
  await ctx3.send(embed=embed)

  categoriesToSave.clear()  


        
@client.command()
@commands.has_permissions(manage_channels=True, administrator=True)
async def SaveCategories(ctx3):


  random_string = ''

  for _ in range(10):
     # Considering only upper and lowercase letters
      random_integer = random.randint(97, 97 + 26 - 1)
      flip_bit = random.randint(0, 1)
    # Convert to lowercase if the flip bit is on
      random_integer = random_integer - 32 if flip_bit == 1 else random_integer
    # Keep appending random characters using chr(x)
      random_string += (chr(random_integer))


  for channel in ctx3.guild.categories:
    categoriesToSave.append(channel)
  
    with open(random_string, "w") as f:
      for s in categoriesToSave:
        f.write(str(s) +"\n")

        #await asyncio.sleep(500)
        #random_string = ""
  with open (str(ctx3.author.id), "a")  as list:
    list.write(f"{ctx3.guild.name} {random_string} categories\n")

  print(random_string)

  embed=discord.Embed(title = 'The categories were save!', color=0x000000)
  embed.add_field(name = "/RestoreCategories +", value = random_string)
  embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
  await ctx3.send(embed=embed)
  categoriesToSave.clear()


@client.command()
@commands.has_permissions(manage_channels=True, administrator=True)
async def SaveVoiceChannel(ctx3):
  random_string = ''

  for _ in range(10):
     # Considering only upper and lowercase letters
      random_integer = random.randint(97, 97 + 26 - 1)
      flip_bit = random.randint(0, 1)
    # Convert to lowercase if the flip bit is on
      random_integer = random_integer - 32 if flip_bit == 1 else random_integer
    # Keep appending random characters using chr(x)
      random_string += (chr(random_integer))


  for channel in ctx3.guild.channels:
    if channel.type == discord.ChannelType.voice:
      VoiceToSave.append(channel)
  
      with open(random_string, "w") as f:
        for s in VoiceToSave :
          f.write(str(s) +"\n")

        #await asyncio.sleep(500)
        #random_string = ""

    else:
      pass
  
  with open (str(ctx3.author.id), "a")  as list:
    list.write(f"{ctx3.guild.name} {random_string} voice channels\n")

  print(random_string)

  embed=discord.Embed(title = 'The voice channels were save!', color=0x000000)
  embed.add_field(name = "/RestoreVoiceChannel +", value = random_string)
  embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
  await ctx3.send(embed=embed)

  categoriesToSave.clear()   

@client.command()
@commands.has_permissions(manage_channels=True, administrator=True)
async def Restore (ctx4, restore):

  with open (restore, "r") as a:
    for s in a:
      #channelToSave.append(channel)
      #print (channelToSave)
      print(s)
      guild = ctx4.channel.guild
      await guild.create_text_channel (s)
  embed=discord.Embed(title = 'Restore!', color=0x000000)
  embed.add_field(name ="```The text channels were restore```")
  embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
  await ctx4.send(embed=embed)

@client.command()
@commands.has_permissions(manage_channels=True, administrator=True)
async def RestoreCategories (ctx4, restore):

  with open (restore, "r") as a:
    for s in a:
      #channelToSave.append(channel)
      #print (channelToSave)
      print(s)
      #guild = ctx4.category.guild
      await ctx4.guild.create_category(s)

  embed=discord.Embed(title = 'Restore!', color=0x000000)
  embed.add_field(name ="```The categories were restore```")
  embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
  await ctx4.send(embed=embed)


@client.command()
@commands.has_permissions(manage_channels=True, administrator=True)
async def RestoreVoiceChannel (ctx4, restore):
  with open (restore, "r") as a:
    for s in a:
      #channelToSave.append(channel)
      #print (channelToSave)
      print(s)
      guild = ctx4.channel.guild
      await guild.create_voice_channel(s)

  embed=discord.Embed(title = 'Restore!', color=0x000000)
  embed.add_field(name ="```The voice channels were restore```")
  embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
  await ctx4.send(embed=embed)


@client.command()
@commands.has_permissions(manage_channels=True, administrator=True)
async def DeleteAll(ctx3):
  for channel in ctx3.guild.channels:
    await channel.delete()


@client.command()
async def BackupList(ctx):
  vuoto = "/HelpChannel"
  embed=discord.Embed(title = 'ListBackup', color=0x000000)

  with open (str(ctx.author.id), "r") as list:
    for codice in list:
      embed.add_field(name = codice, value = f"{vuoto}" )
  
  embed.set_image(url="https://media.discordapp.net/attachments/709013169842159626/811532032390987816/tenor.gif")
  await ctx.send(embed=embed)
  
keep_alive()

client.run(os.environ['TOKEN'])
