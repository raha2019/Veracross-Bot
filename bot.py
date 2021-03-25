import discord
from discord.ext import commands
from homework import *


client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    # if message.content.startswith('!setup'):
    #     await member.dm_channel.send("Use !email to setup email and !pass to setup pass")
    # if message.content.startswith('!email'):



    # # if message.content.startswith('!hw'):

    #     await message.channel.send(get_homework('rahul.gupta@austinprep.org', 'R@h@2213'))

@client.command(name='setup')
async def setup(ctx, arg1: str, arg2: str):
    update_creds(int(ctx.message.author.id), str(arg1), str(arg2))
    await ctx.send("Your creds have been recorded.")
    
@client.command(name='hw')
async def hw(ctx): # (make arguments strings)
    if not check_credentials_exist(int(ctx.message.author.id)): # Test this too
        await ctx.send("Sorry no credential exist, please use the !setup command to enter your credentials.")
        return 

    print(check_valid_credentials(int(ctx.message.author.id)))
    if not check_valid_credentials(int(ctx.message.author.id)):
        await ctx.send("Your credentials are invalid, change them with !setup.")
        return 

    email, password = get_creds(int(ctx.message.author.id))
    await ctx.send(get_homework(email, password))


client.run('ODI0MTA3NTYxNTkzODY0MTky.YFqj-Q.sbxtvpcdIEIgyX325rMm7Id3FVk')