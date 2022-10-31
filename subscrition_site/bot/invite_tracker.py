from discord.ext import commands
import discord
import DiscordUtils



class InviteTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tracker = DiscordUtils.InviteTracker(bot)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        inviter = await self.tracker.fetch_inviter(member)
        data = await self.bot.invites.find_by_custom(
            {"guild_id": member.guild.id, "inviter_id": inviter.id}
        )
        if data is None:
            data = {
                "guild_id": member.guild.id,
                "inviter_id": inviter.id,
                "count": 0,
                "invited_users": []
            }

        data["count"] += 1
        data["invited_users"].append(member.id)
        await self.bot.invites.upsert_custom(
            {"guild_id": member.guild.id, "inviter_id": inviter.id}, data
        )

        channel = discord.utils.get(member.guild.text_channels, name="recording")
        embed = discord.Embed(
            title=f"Welcome {member.display_name}!",
            description=f"Invited by: {inviter.mention}\nInvites: {data['count']}",
            timestamp=member.joined_at,
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
        await channel.send(embed=embed)
def setup(bot):
    bot.add_cog(InviteTracker(bot))