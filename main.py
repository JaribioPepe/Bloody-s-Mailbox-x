import asyncio
import os
import platform
import random
import time
from collections import Counter
from replit import db
import discord
import praw
import pytz
from discord.ext import commands
import feedparser

from keep_alive import keep_alive

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True
intents.reactions = True

client = commands.Bot(command_prefix="$", intents=intents)

@client.event
async def on_ready():
    print("Bot's Ready")
    if not db.get("WATCHED"):
        db["WATCHED"] = {}
    if not db.get("TO_BAN"):
        db["TO_BAN"] = []
    CHANNEL = client.get_channel(932174655316455434)
    await client.change_presence(activity=discord.Streaming(
        name="Gaming_Setups", url="https://www.youtube.com/watch?v=l7XKNoOMYro&list=PLy4Nh_R3CRVQltP5xM1K7-V0DrQcAlqHT")
                                 )
    while True:
        # guildCount = len(client.guilds)
        # memberCount = len(list(client.get_all_members()))
        # randomGame = random.choice(games)
        # await client.change_presence(
        #     activity=discord.Activity(
        #         type=randomGame[0],
        #         name=randomGame[1].format(guilds=guildCount, members=memberCount),
        #     )
        # )
        ANCHOR = feedparser.parse("https://anchor.fm/s/55d22f30/podcast/rss")
        FEEDS = [ANCHOR]
        for feed in FEEDS:
            entry = feed.entries[0]
            message = f"@here Find more of Us from https://linktr.ee/254millennialtalk \nCatch up with yesterday's show on your favorite podcast platform of choice {entry.link}"
            value = db.get(entry.title)
            if not value:
                db[entry.title] = entry.link
                await CHANNEL.send(message)
        await asyncio.sleep(1)
        db["WATCHED"] = {}


@client.command()
async def posts(ctx, number_of_posts: int = 60):
    ANCHOR = feedparser.parse("https://anchor.fm/s/55d22f30/podcast/rss")
    entries = ANCHOR.entries[:number_of_posts]
    if number_of_posts == 1:
        entry = ANCHOR.entries[0]
        await ctx.send(entry.link)
    else:
        embed = discord.Embed(title=entries[0].author)
        for entry in entries:
            embed.add_field(name=entry.title, value=entry.link)
        await ctx.send(embed=embed)


@client.command()
async def hello(ctx):
    await ctx.send("Hello " + str(ctx.author.display_name) + ", What's up?")


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx):
    keys = db.keys()
    posts = len(keys)
    for key in keys:
        del db[key]
    await ctx.send(f"All {posts} post(s) have been cleared")


@client.event
async def on_message(message):
    empty_array = []
    modmail_channel = discord.utils.get(client.get_all_channels(),
                                        name="💌-↣｜mailbox")
  
    if message.author == client.user:
        return
    bot = discord.ClientUser.bot
    if message.author is bot:
        return

    if str(message.channel.type) == "private":
        if message.attachments != empty_array:
            files = message.attachments
            await modmail_channel.send("[" + message.author.mention + "]")
            await message.channel.send(
                f" Yoh 👋🏾, {message.author.mention} The Staff will get back to you When they get to See your message"
            )
            for file in files:
                await modmail_channel.send(file.url)

        else:
            await modmail_channel.send("[" + message.author.mention + "] " +
                                       message.content)
            await message.channel.send(
                f" Yoh👋🏾, {message.author.mention} The Staff will get back to you When they get to See your message "
            )
    elif str(message.channel) == "💌-↣｜mailbox" and message.content.startswith(
            "<"):
        member_object = message.mentions[0]
        if message.attachments != empty_array:
            files = message.attachments

            for file in files:
                await member_object.send(file.url)
        else:
            index = message.content.index(" ")
            string = message.content
            mod_message = string[index:]
            await member_object.send(mod_message)

    guild_id = message.guild.id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    role = discord.utils.get(guild.roles, id=843790234335445012)


  

keep_alive()
client.run(os.getenv("token"))
