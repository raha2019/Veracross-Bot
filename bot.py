import discord
from discord.ext import commands
from homework import *


client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command(name='setup')
async def setup(ctx, arg1: str, arg2: str):
    update_creds(int(ctx.message.author.id), str(arg1), str(arg2))
    await ctx.send("Your creds have been recorded.")
    
@client.command(name='hw')
async def hw(ctx): # (make arguments strings)

    # Check if the credentals exist
    embed = discord.Embed(title="Homework Status")
    embed.set_author(name="Veracross Bot", url="https://github.com/raha2019/Veracross-Bot", icon_url="https://pbs.twimg.com/profile_images/1323667180299440128/INS15fm1.jpg")
    embed.add_field(name="Progress", value="1/3", inline=True)
    embed.set_footer(text="Checking if your credentials exist")
    
    message = await ctx.send(embed=embed)

    if not check_credentials_exist(int(ctx.message.author.id)): # Test this too
        await ctx.send("Sorry no credential exist, please use the !setup command to enter your credentials.")
        return 
    
    # Check if the credentials are valid
    embed = discord.Embed(title="Homework Status")
    embed.set_author(name="Veracross Bot", url="https://github.com/raha2019/Veracross-Bot", icon_url="https://pbs.twimg.com/profile_images/1323667180299440128/INS15fm1.jpg")
    embed.add_field(name="Progress", value="2/3", inline=True)
    embed.set_footer(text="Checking if your credentials are valid")
    await message.edit(embed=embed)             
    if not check_valid_credentials(int(ctx.message.author.id)):
        await ctx.send("Your credentials are invalid, change them with !setup.")
        return 

    # Get assignments
    embed = discord.Embed(title="Homework Status")
    embed.set_author(name="Veracross Bot", url="https://github.com/raha2019/Veracross-Bot", icon_url="https://pbs.twimg.com/profile_images/1323667180299440128/INS15fm1.jpg")
    embed.add_field(name="Progress", value="3/3", inline=True)
    embed.set_footer(text="Getting your assignments")
    await message.edit(embed=embed)     

    email, password = get_creds(int(ctx.message.author.id))
    await ctx.send(get_homework(email, password))
    # x = 0
    # while x <= arg1:
    #     await ctx.send(get_homework(email, password))
    #     x += 1


client.run('XXXXXX')