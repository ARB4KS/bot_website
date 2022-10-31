
from datetime import datetime, timedelta
import discord
import random
from discord.utils import get
from discord.ext import commands
#from dateutil.relativedelta import relativedelta
from bot.invite_tracker import setup
import sqlite3
#from bot.database import Database
import sched, time
import DiscordUtils
#a = Database

intents = discord.Intents.all()
intents.members = True
TOKEN = "MTAzNjI5NjU5NjI4OTI0NTIzNQ.GNx8AK.I8e-3s4uMP8hxtW3NnXmbBfQdv-eUolIDh4Wk4"
client = commands.Bot(intents=discord.Intents.all(), command_prefix="!")
tracker = DiscordUtils.InviteTracker(client)

def run():
    client.run(TOKEN)

@client.command(pass_context=True)
async def kick(ctx, user: discord.Member):
    get_user = client.get_user(user.id)
    link = await ctx.channel.create_invite(max_age=300)
    await ctx.message.author.kick()


@client.event
async def on_member_join(member):
    channel = client.get_channel(1034157735564017668)
    new_invites = await member.guild.invites()
    for i in range(len(new_invites)):

        inviter = new_invites[i].inviter
        uses = new_invites[i].uses
    await channel.send(f"{member} joined the server with {inviter}'s invite, they have invited {uses} members")
    old_invites = new_invites

@client.event

async def on_message(message):
    await client.process_commands(message)
    return False




