import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import time
import pprint as pp

load_dotenv()
TOKEN = os.getenv("SCAV_TOKEN")

# Setup Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    for guild in bot.guilds:
        for channel in guild.channels:
            print(channel)

@bot.command(pass_context=True)
async def voicechannels(ctx):
    channels = (c.name for c in ctx.message.server.channels if c.type==ChannelType.voice)
    await bot.say("\n".join(channels))

@bot.command()
async def channels(ctx):
    voice_channel_list = ctx.guild.voice_channels # creates a list of voice channels of class 'discord.channel.VoiceChannel'
    # import pdb; pdb.set_trace()
    await ctx.send("Printing list")
    formatted_channels = ""
    for channel in voice_channel_list:
        formatted_channels = formatted_channels + channel.name + '\n'
    await ctx.send(formatted_channels)
    print(voice_channel_list)

@bot.command()
async def scav(ctx):
    # get list of channels
    voice_channel_list = ctx.guild.voice_channels # creates a list of voice channels of class 'discord.channel.VoiceChannel'
    
    await ctx.send("Printing list")
    formatted_channels = ""
    for channel in voice_channel_list:
        formatted_channels = formatted_channels + channel.name + " - position: " + str(channel.position) + '\n'
    await ctx.send(formatted_channels)
    # import ipdb; ipdb.set_trace()
    # channel = await bot.create_voice_channel("Emercom Medical Unit")
    # channel = await ctx.guild.create_text_channel('cool-channel')

    channel = await ctx.guild.create_voice_channel("Emercom Medical Unit")

    voice_channel_list = ctx.guild.voice_channels
    last_vc_position = voice_channel_list[-1].position # gets the last voice channel position 

    await channel.edit(position=last_vc_position + 1)
    # TODO add category moving support

    # select target of connected users 
    # voice_channel_list


    import ipdb; ipdb.set_trace()

    # await fetch_channel(channel_id)

    time.sleep(5)
    # make sure to clean up when done
    await channel.delete()


@bot.command()
async def voice(ctx):
    VC = discord.utils.get(ctx.guild.channels, id=705524214270132368)
    print(VC.members)  # each user is a member object
    for user in VC.members:
        # Code here
        print(user.name)

@bot.command()
async def lmem(ctx): # list members ids connected to voice channels
    connected_users = []
    voice_channel_list = ctx.guild.voice_channels # list of voice channels
    for channel in voice_channel_list:
        # print("{} has {} members ".format(channel.name, channel.voice_states))
        [connected_users.append(i) for i in iter(channel.voice_states)]
    await ctx.send(str(connected_users))


# !scav
# get list of channels
# make channel at bottom with a list of random names - Emercom Medical Unit, Old Gas, New Gas, Mantis etc
# select target of connected users 
# move 1 channel closer to target based on different time periods, expand later, use 1-5 seconds for testing 
# keep track of state - channels and users
# if bot joins channel with target, create a new channel, play a scav sound effect and delete the channel


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
    # for guild in bot.guilds:
    #     for channel in guild.channels:
    #         print(channel)
            # print(voice_clients)






bot.run(TOKEN)

