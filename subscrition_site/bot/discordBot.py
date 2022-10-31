
from datetime import datetime, timedelta
import discord
import random
from discord.utils import get
from discord.ext import commands
from dateutil.relativedelta import relativedelta
import sqlite3
#from bot.database import Database
import sched, time

#a = Database

intents = discord.Intents.all()
intents.members = True
TOKEN = "MTAzNjI5NjU5NjI4OTI0NTIzNQ.GzWLLp.HCfZ0XaeNiYaVHfR8b-g7lh3PMhnJaLJShWdIs"
client = commands.Bot(intents=discord.Intents.all(), command_prefix="!")


def run():
    client.run(TOKEN)
# @client.event
# async def on_member_join(member):
#   guild = client.get_guild(939513182505037894)
#   print(guild)
#   new_date = date_object + timedelta(days=2)
#   channel = client.get_channel(1025489828709683292)
#   print(new_date)
#   message = member.name + " Test valable jusqu'au " + str(new_date)
#   role = discord.utils.get(guild.roles, id=1025757565151363072)
#   print(role)
#   check = a.add_test_user(member.id, new_date)
#   channel = client.get_channel(1025489828709683292)
#   if check == 5:
#     await channel.send(f"L'utilisateur {member.mention} a dêjà fait son test.")
#
#   elif check == True:
#     await channel.send("Client dêjà enregistré dans la base de données ")
#
#   else:
#     print(member)
#     await channel.send(message)
#     await member.add_roles(role)
class RunBot(commands.Bot):
    def get_date(self):
        now = datetime.now()
        date_time_str = now.strftime("%d/%m/%Y")
        date_object = datetime.strptime(date_time_str, '%d/%m/%Y').date()
        return date_object


    @client.command(pass_context=True)
    async def add_client(self,ctx, user: discord.Member):
        date = get_date()
        channel = client.get_channel(1027987441438687262)
        new_date = date + relativedelta(months=+1)
        message = user.name + " Abonnement valable jusqu'au " + str(new_date)
        role = discord.utils.get(ctx.guild.roles, id=1015989912920658062)
        print(role)
        check = a.execute(user.id, new_date)
        words = ctx.message.content.split()
        size = len(words)

        if check == True:
            await channel.send("Client dêjà enregistré dans la base de données ")
            return
        if size > 2:
            parrain_check = a.ajout_parrain(ctx.message.mentions[1].id)
        if user is None:
            member = ctx.author
        print(user)
        await channel.send(message)
        await user.add_roles(role)


    @client.command(pass_context=True)

    async def reset_parrain(self,ctx, user: discord.Member):
        id_parrain = user.id
        channel = client.get_channel(1027987441438687262)
        check = a.reset_parrain(user.id)
        if check == False:
            await channel.send("Cette personne n'est pas enregistrée")
            return
        await channel.send("L'argent a été remis à zéro")


    # @client.command(pass_context=True)
    # async def list_parrain(ctx):


    @commands.has_role("Admin")
    @staticmethod

    @client.command(pass_context=True)
    async def prolongate(ctx, user: discord.User):
        new_date = a.prolong(user.id)
        await ctx.send(f" Abonnement de {user.name} prolongé jusqu'au {new_date}")


    @commands.has_role("Admin")
    @client.command()
    async def members(self,ctx):
        channel = client.get_channel(1027988513439875163)
        server = ctx.guild
        test_role = discord.utils.get(server.roles, id=1015990431919656982)
        role = discord.utils.get(server.roles, id=1015989912920658062)

        for guild in client.guilds:
            for member in guild.members:

                check = a.check_if_registered(member.id)
                date_check = a.end_date(member.id)

                check_test = a.check_if_registered_test(member.id)
                if check_test == 5:
                    await member.remove_roles(test_role)
                    a.blacklist_test(member.id)
                    await channel.send(
                        f"{member.mention} ton test a expiré, on espère que tu es satisfait du prenium !")

                if role in member.roles:
                    if check == True:
                        await channel.send(
                            f"{member.mention} ton abonnement à expiré, il faut que tu le renouvelle")
                        await member.remove_roles(role)
                    if date_check != False:
                        await channel.send(
                            f"{member.mention} ton abonnement expire le {date_check} pense à le renouveller bientôt")


    @commands.has_role("Admin")
    @client.command()
    async def add_client_test(self,ctx, user: discord.Member):
        date = get_date()
        new_date = date + timedelta(days=2)
        print(new_date)
        message = user.name + " Test valable jusqu'au " + str(new_date)
        role = discord.utils.get(ctx.guild.roles, id=1015990431919656982)
        check = a.add_test_user(user.id, new_date)
        if check == 5:
            await ctx.send(f"L'utilisateur {user.name} a dêjà fait son test.")

        elif check == True:
            await ctx.send("Client dêjà enregistré dans la base de données ")
        elif user is None:
            member = ctx.author
        else:
            print(user)
            await ctx.send(message)
            await user.add_roles(role)


    @commands.has_role("Admin")
    @client.command()

    async def members_test(self,ctx):
        server = ctx.guild
        role = get(server.roles, id=1025092370120839278)
        for guild in client.guilds:
            for member in guild.members:
                check = a.check_if_registered_test(member.id)
                if check != False:
                    await member.remove_roles(role)
                    a.blacklist_test(member.id)


    @commands.has_role("Admin")
    async def on_message(self,message):
        await client.process_commands(message)
        return False



