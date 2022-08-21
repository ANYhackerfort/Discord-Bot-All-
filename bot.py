import asyncio
from tabnanny import check
import discord
import random 
import os 
import pandas as pd
from discord.ext import commands 
import tracemalloc
import time 
from datetime import datetime
from tokenize import String
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from fpdf import FPDF
import io
from PIL import Image
import matplotlib.pyplot as plt

now = str(datetime.now())
now = now[0:10]
tracemalloc.start()

TOKEN = 'MTAwOTMyMDY5NDI1OTEzODU4MA.GntKxY.4Bp5CzVBhyrXBRWQPF_3pGJovxqOzFqU7RytkI' #DSAV
# TOKEN = 'MTAxMDMyNjk3NDUyNDI5NzMwNw.GEDO04.Jgm6WQujA7lLbNSLAMp-9CElHgE72aC3Cww_aM' #Tony's
client = discord.Client() 
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '.', intents=intents)
#flask 
@client.event 
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return 
    if message.content.startswith('$hello'):
        await message.channel.send('Hi!')
        
        return
    if message.content.startswith('$notJoinedMembers'):
        await message.channel.send('Getting List from Google Document!')
        #get giffy from doc transfered... under progress
        await message.channel.send('...')
        await message.channel.send('Not Found!')
    await client.process_commands(message)

# async def get_members(guild_id, channel_id):

@client.command()
# async def ping():
#     try:
#         msg = await client.wait_for("message", check=check, timeout=20)
#     except asyncio.TimeoutError:
#         await client.say("Sorry, you did not reply in time!")
async def ping(ctx):
    await ctx.send('Pong!')
@client.command()
async def log(ctx): 
    await ctx.send('Returning Log!')
@client.command()
async def spotifyArtists(ctx, string): 
    await ctx.send('Checking your playlist...')
    client_credentials_manager = SpotifyClientCredentials(client_id='ed5cbf589898495db2525f4a918ecdd5', client_secret='cc6ae854428c4a139ccc4c1a5d955ff7')
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    playlist_link = str(string)
    playlist_URI = playlist_link.split("/")[-1].split("?")[0] 
    trackUrl = [] 
    trackName = [] 
    doubleNames = []

    def getIDName():
        for track in sp.playlist_tracks(playlist_URI)["items"]:
            track_uri = track["track"]["uri"]
            track_name = track["track"]["name"]
            trackUrl.append(str(track_uri))
            trackName.append(str(track_name))

        doubleNames = list(zip(trackUrl, trackName)) 
        return doubleNames 

    def getUri():
        track_uri = sp.playlist_tracks(playlist_URI)["items"]
        id = [] 
        for item in track_uri:
            track = item['track']
            id.append(track['id'])
        return id

# print(getUri())
    def artistNames(list):
        names = [] 
        for item in list:
            meta = sp.track(item)
            name = meta['name']
            names.append(name)
        return names 
    def speechinesss(list):
        speeches = [] 
        piano = 0
        duol = 0
        all = 0 
        for item in list:
            features = sp.audio_features(item)
            speech = features[0]['danceability']
            print(speech)
            if speech < 0.33:
                piano += 1
            if 0.33 <= speech < 0.66:
                duol += 1
            if 0.66 <= speech < 0.99:
                all += 1 
            

        listz = [piano, duol, all]
        print(listz)
        j = listz[0] 
        placement = 0 
        for item in listz:
            if item > j:
                j = item
                placement += 1
            else:
                continue 
        list2 = ["calm music", "songs to vibe to", "head bangers"]
        print(list2)
        plt.bar(list2, listz, color='black')
        plt.xlabel("Type of Music")
        plt.ylabel("Number of Tracks in Category")
        bob = str(ctx.message.guild.get_member(ctx.message.author.id)) + str(" Specified Playlist")
        plt.title(bob)
        print(ctx.message.guild.get_member(ctx.message.author.id))
        # plt.show() 
        img_buf = io.BytesIO()
        plt.savefig('graph.png')
        # im = Image.open(img_buf)
        # im.show(title="graph")
        return str(list2[placement])

        
        speeches.append(speech)

    
    # await ctx.send(artistNames(getUri()))
    await ctx.send("Most of your songs are " + speechinesss(getUri()))
    await ctx.send(file = discord.File("graph.png"))
    os.remove("graph.png")
    # for item in artistNames(getUri()):
    #     await ctx.send(str(item))

@client.command()
async def echo(ctx, string):
    output = string.split(", ")
    echo.getOutput = output 
    await ctx.send(output)
    for item in output:
        await ctx.send(str(item))

@client.command()
async def memberList(ctx):
    await ctx.send(echo.getOutput) 

@client.command()
async def getRole(ctx):
    member = ctx.message.author
    role = discord.utils.get(member.guild.roles, name='Members')
    await member.add_roles(role)

@client.event
async def on_member_join(member):
    guild_id = member.guild.id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    memberID = member.id 
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True),
    }
    channel = await guild.create_text_channel(str(memberID), overwrites=overwrites, category=guild.get_channel(1010467763778768906))    
    for channel in member.guild.channels:
        if str(channel) == str(memberID):
            await channel.send(f"""Welcome to the Discord Server {member.mention}! \nYou joined on {str(now)}. Make sure you have read our rules and services. Let's get started on making you part of the team!""")
            retStr = str("""```css\n 🥼 for activities \n 🔬 for mentorship \n 📸 for marketing \n 📥 for communications```""")
            embed = discord.Embed(title="Please react below to be assigned to your division!")
            embed.add_field(name="ASCEF",value=retStr)
            msg = await channel.send(embed=embed)
            await msg.add_reaction('🥼')
            await msg.add_reaction('🔬')
            await msg.add_reaction('📸')
            await msg.add_reaction('📥')
            embed2 = discord.Embed(title="Information Regarding your private channel: ")
            retStr2 = str("""```This channel is unique to you \nand you are the only one that has access to it disregarding the bot and admins. \nHere is the place where you can contact admins to ask private questions or get commonly asked questions through the bot! \nclick the 👍 to see full list of commands! \nChannel will delete after you leave the server to protect your personal online data!```""")
            embed2.add_field(name="ASCEF",value=retStr2)
            msg2 = await channel.send(embed=embed2)
            await msg2.add_reaction('👍')

    # time.sleep(28)
@client.event
async def on_member_remove(member):
    guild_id = member.guild.id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    for channel in member.guild.channels:
        memberID = member.id
        if str(channel) == str(memberID):
            await channel.delete()

@client.event
async def on_raw_reaction_add(payload):
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    member = discord.utils.get(guild.members, id=payload.user_id)
    if payload.emoji.name == "🥼":
        role = discord.utils.get(guild.roles, name="Activities")
        await member.send("You have Selected Activities Branch! ")
        await member.add_roles(role)
    if payload.emoji.name == "🔬":
        role = discord.utils.get(guild.roles, name="Mentorship")
        await member.send("You have Selected Mentorship Branch! ")
        await member.add_roles(role)
    if payload.emoji.name == "📸":
        role = discord.utils.get(guild.roles, name="Marketing")
        await member.send("You have Selected Marketing Branch! ")
        await member.add_roles(role)
    if payload.emoji.name == "📥":
        role = discord.utils.get(guild.roles, name="Communications")
        await member.send("You have Selected Communications Branch! ")
        await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    member = discord.utils.get(guild.members, id=payload.user_id)
    if payload.emoji.name == "🥼":
        role = discord.utils.get(guild.roles, name="Activities")
        await member.send("You have unselected Activities Branch! ")
        await member.remove_roles(role)
    if payload.emoji.name == "🔬":
        role = discord.utils.get(guild.roles, name="Mentorship")
        await member.send("You have unselected Mentorship Branch! ")
        await member.remove_roles(role)
    if payload.emoji.name == "📸":
        role = discord.utils.get(guild.roles, name="Marketing")
        await member.send("You have unselected Marketing Branch! ")
        await member.remove_roles(role)
    if payload.emoji.name == "📥":
        role = discord.utils.get(guild.roles, name="Communications")
        await member.send("You have unselected Communications Branch! ")
        await member.remove_roles(role)


# @client.command()
# async def getRole(ctx, string):
#     role = get(member.guild.roles, name='')
#     await ctx.send('')
#     if string == '11':

#     if string == '10':
#     if string == '9':
#     if string == '12':


        
    
client.run(TOKEN)
print("ran")