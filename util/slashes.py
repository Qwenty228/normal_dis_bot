from discord.user import ClientUser
from discord_slash import SlashContext, cog_ext, SlashCommandOptionType as SOT
from discord_slash.utils.manage_commands import create_option, create_choice
from discord.ext import commands
import discord, os
from util.functions import amiya, rabbit_hump
from datetime import datetime
from env import guild_ids



class Slashes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="guild", description="Get Guild Metainfo", guild_ids=guild_ids
    )
    async def _guild(self, ctx: SlashContext):
        guilds = self.bot.guilds
        await ctx.send(str(guilds))

    @cog_ext.cog_slash(
        name="ping", description="Ping Pong 遊ぼう!", guild_ids=guild_ids
    )
    async def _ping(self, ctx: SlashContext):
        interval = datetime.utcnow() - ctx.created_at
        await ctx.send(
            f"Pong! Ping = {interval.total_seconds() * 1000} ms"
        )

    @cog_ext.cog_slash(
        name="kamui", description="Clear Messages to delete what you have done", guild_ids=guild_ids,
        options=[
            create_option(
                name="clear_amount",
                description="How many messages to Purge",
                option_type=10,
                required=True
            )
        ]
    )
    async def _cleara(self, ctx: SlashContext, clear_amount: str):
        await ctx.send("**japanese word!!!**")

        await ctx.channel.purge(limit=int(clear_amount) + 1)

        await ctx.send(f"even more **{clear_amount}** japanese that I dont understand!!!")
        await ctx.channel.send("https://c.tenor.com/xexSk5SQBbAAAAAC/discord-mod.gif")

    @cog_ext.cog_slash(
        name="blep", description="No one have idea what command is this", guild_ids=guild_ids,
        options=[
            create_option(
                name="person",
                description="Who you want to B L E P",
                required=True,
                option_type=6),
            create_option(
                name="which",
                description='bullying with gif',
                required=False,
                option_type=3,
                choices=[create_choice(name="amiya", value="a"),
                        create_choice(name="mick", value="h")]
            )
        ]
    )
    async def _blep(self, ctx: SlashContext, person: str, which="a"):
        await ctx.defer()
        pfp = await person.avatar_url_as(format="png").read()
        if which=="a":
          amiya(pfp)
        elif which=="h":
          rabbit_hump(pfp)
        embed = discord.Embed(title="stonk", description="mick is horuni", color=0x00ff00) #creates embed
        file = discord.File('./util/assets/done.gif')
        embed.set_image(url="attachment://done.gif")
        embed.set_author(name=person.name)
        embed.set_footer(text="amiya")
        await ctx.send(file=file, embed=embed)


    @cog_ext.cog_slash(
        name="gay", description="Insult someone for being gae", guild_ids=guild_ids,
        options=[
             create_option(
                 name="person",
                 description="Who to insult",
                 required=False,
                 option_type=SOT.USER
             )
        ]
    )
    async def _gay(self, ctx: SlashContext, person: ClientUser = None):
        if person is None:
            await ctx.send(f"<@!{ctx.author_id}> is gay!")

        await ctx.send(f"{person.mention} is gay!")
