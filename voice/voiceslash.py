from discord_slash import  SlashContext, cog_ext, ComponentContext
from discord_slash.utils.manage_commands import create_choice, create_option
import discord, os
from discord.ext import commands
from voice.ytdlstuff import YTDLSource1
from random import choice


guild_ids = [int(id) for id in os.environ['guild_ids'].split(',')]


class Vslash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @cog_ext.cog_slash(name="thorns",description="gay", guild_ids=guild_ids)
    async def _thorns(self, ctx:SlashContext):
        if not ctx.voice_client:
            channel = ctx.author.voice.channel
            await channel.connect()
        if ctx.voice_client.is_playing():
          ctx.voice_client.pause()
          #return await ctx.send("currently playing")
        url = choice(["https://aceship.github.io/AN-EN-Tags/etc/voice/char_293_thorns/CN_028.mp3", "https://aceship.github.io/AN-EN-Tags/etc/voice/char_293_thorns/CN_026.mp3"])
        await ctx.defer()
        player = await YTDLSource1.from_url(url=url, loop=self.bot.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        embed = discord.Embed(title=f"chi", color=discord.Color.blurple())
        embed.set_image(url="https://media.discordapp.net/attachments/515423288114151425/878336201675923507/image0.gif")
        await ctx.send(embed=embed)

        if ctx.voice_client.is_paused():
          print(ctx.voice_client.source)
