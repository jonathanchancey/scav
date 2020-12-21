import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import time
import pprint as pp
import random
import asyncio
import glob
from datetime import datetime, timedelta


# if not discord.opus.is_loaded():
#     # the 'opus' library here is opus.dll on windows
#     # or libopus.so on linux in the current directory
#     # you should replace this with the location the
#     # opus library is located in and with the proper filename.
#     # note that on windows this DLL is automatically provided for you
#     discord.opus.load_opus('opus')

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

async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice


# @play.before_invoke
# @yt.before_invoke
# @stream.before_invoke
# async def ensure_voice(self, ctx):
#     if ctx.voice_client is None:
#         if ctx.author.voice:
#             await ctx.author.voice.channel.connect()
#         else:
#             await ctx.send("You are not connected to a voice channel.")
#             raise commands.CommandError("Author not connected to a voice channel.")
#     elif ctx.voice_client.is_playing():
#         ctx.voice_client.stop()
# TODO rewrite as class with voice functions that make sense
class Scav(commands.Cog):
    def __init__(self, bot):
        # spawn channel names list
        self.spawn_channel_names = ['Emercom Medical Unit', 'KIBA Arms', 'Old Gas', '3rd Floor Dorms', 'ZB-1014']
        # temp channel names list
        self.temp_channel_names = [';-;', '💀', '😵', '(✖╭╮✖)']
        # sound effect names list
        cwd = os.getcwd()
        self.sound_effect_paths = glob.glob('effects/*.mp3')
        print("self.sound_effect_paths = {} \n cwd = {}".format(self.sound_effect_paths, cwd))

        

        self.bot = bot
    
    async def cleanup_scav(self, ctx, seconds_back):
        # look for channels created in the past minute with spawn or temp channel names
        voice_channel_list = ctx.guild.voice_channels
        present = datetime.now()
        for channel in voice_channel_list:
            if channel.created_at - present < timedelta(seconds=seconds_back): # if the channel was created less than a minute ago
                if channel in self.spawn_channel_names or channel in self.temp_channel_names: # and if the name matches 
                    await channel.delete()
            

    @commands.command()
    async def clean(self, ctx):
        await self.cleanup_scav(ctx, 300)


    @commands.command()
    async def scav(self, ctx):
        """Hunt down a random member"""
        
        # get list of channels
        voice_channel_list = ctx.guild.voice_channels # creates a list of voice channels of class 'discord.channel.VoiceChannel'
        
        # await ctx.send("Printing list")
        formatted_channels = ""
        for channel in voice_channel_list:
            formatted_channels = formatted_channels + channel.name + " - position: " + str(channel.position) + '\n'
        # await ctx.send(formatted_channels)
        # import ipdb; ipdb.set_trace()
        
        channel = await ctx.guild.create_voice_channel(random.choice(self.spawn_channel_names))

        voice_channel_list = ctx.guild.voice_channels
        last_vc_position = voice_channel_list[-1].position # gets the last voice channel position 

        await channel.edit(position=last_vc_position + 1)
        # TODO add category moving support

        # select target of connected users 
        connected_users = []
        voice_channel_list = ctx.guild.voice_channels # list of voice channels
        for channel in voice_channel_list:
            # print("{} has {} members ".format(channel.name, channel.voice_states))
            [connected_users.append(i) for i in iter(channel.voice_states)]
        # await ctx.send(str(connected_users))
        

        target = random.choice(connected_users)
        print(target)

        # target = await ctx.guild.fetch_member(target)
        target = await ctx.guild.fetch_member(152973904221175808) # TODO REMOVE OVERRIDE
        # print(target)

        if target.voice.channel is None:
            await ctx.send("не может найти цель в голосовом канале")
            # TODO cleanup
            return
        await ctx.send("кто-то сегодня умирает")
        # await ctx.send(str(target.name))

        # join created channel
        voice_client = await channel.connect()

        # get scav and target channel position
        target_channel = target.voice.channel
        target_pos = target_channel.position
        # scav_pos = channel.position - 1
        scav_pos = 6 # TODO REMOVE OVERRIDE

        scav = await ctx.guild.fetch_member(bot.user.id)
        # import ipdb; ipdb.set_trace()
        while scav_pos != target_pos:
            # sanity checks

            # move 1 channel towards target 
            if scav_pos > target_pos:
                channel = voice_channel_list[scav_pos - 1]
            else:
                channel = voice_channel_list[scav_pos + 1]
            await asyncio.sleep(1) 

            print("target pos = {} \n scav pos = {}".format(target_pos, scav_pos))
            print("joining {}".format(channel.name))
            try: 
                await scav.move_to(channel)
            except Exception as inst:
                print(inst)
                print("ERROR: Could not move scav") # TODO cleanup function
                if scav_pos > target_pos:
                    channel = voice_channel_list[scav_pos - 2]
                else:
                    channel = voice_channel_list[scav_pos + 2]
                try: 
                    await scav.move_to(channel)
                except:
                    pass
                
                continue

            # refresh state
            voice_channel_list = ctx.guild.voice_channels # list of voice channels
            scav_pos = channel.position
            target_pos = target_channel.position
        
        
        # create channel 
        temp_channel = await ctx.guild.create_voice_channel(random.choice(self.temp_channel_names))
        await temp_channel.edit(position=0)
        # move target and scav in channel

        if ctx.voice_client is not None:
                await ctx.voice_client.move_to(temp_channel)

        print("Attempting to move SCAV to {}".format(temp_channel))
        await scav.move_to(temp_channel)

        print("Attempting to move TARGET to {}".format(temp_channel))
        await target.move_to(temp_channel)
        
        
        # play scav sound
        sound_file_path = random.choice(self.sound_effect_paths)
        print("sound_file_path = {}".format(sound_file_path))
        source = await discord.FFmpegOpusAudio.from_probe(sound_file_path, method='fallback')
        await asyncio.sleep(1) # TODO fix lazy sleep bandaid
        # ctx.voice_client.play(source)
        try:
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            
        # time.sleep(3) # TODO find duration of file
        await asyncio.sleep(3)
        # delete channel 
        # await temp_channel.delete() # !NO

        # make sure to clean up when done
        # await channel.delete() # !NO
        await self.cleanup_scav(ctx, 60)

        try: 
            await ctx.voice_client.disconnect()
        except: 
            print("scav has been disconnected in channel deletion successfully")

@bot.command()
async def lmem(ctx): # list members ids connected to voice channels
    connected_users = []
    voice_channel_list = ctx.guild.voice_channels # list of voice channels
    for channel in voice_channel_list:
        # print("{} has {} members ".format(channel.name, channel.voice_states))
        [connected_users.append(i) for i in iter(channel.voice_states)]
    await ctx.send(str(connected_users))


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
    bot.add_cog(Scav(bot))
    # for guild in bot.guilds:
    #     for channel in guild.channels:
    #         print(channel)
            # print(voice_clients)


bot.run(TOKEN)

