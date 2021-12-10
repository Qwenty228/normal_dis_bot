from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
import discord
from env import guild_ids
import math
import voice.settings as con
import asyncio
from voice.ytdlstuff import Song, YTDLSource




Song_queue = {}

# Silence useless bug reports messages


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.loop = None
        self.song = {}

    async def play_nexts_song(self, ctx):
        global Song_queue
        player = ctx.voice_client
        server_id = ctx.voice_client.server_id if ctx else None
        if self.loop[server_id] and self.song[server_id]:
            source = await YTDLSource.create_source(ctx, self.song[server_id].url)
            Song_queue[server_id].append(source)
        if (Song_queue[server_id] != [] and server_id):
            self.song[server_id] = Song_queue[server_id].pop(0)
            #print([x.title for x in Song_queue[server_id]])
            player.play(self.song[server_id], after=lambda x=None: asyncio.run(
                self.play_nexts_song(ctx)))
        else:
            return
 
    @cog_ext.cog_slash(
        name="join", description="Join Voice Chat", guild_ids=guild_ids, options=[
            create_option(
                name="channel", description="Voice Channel to join", required=False, option_type=3
            )
        ]
    )
    async def _join(self, ctx: SlashContext, *, channel: str = None):
        destination = channel or ctx.author.voice.channel
        if ctx.voice_client:
            return await ctx.voice_client.move_to(destination)
        else:
            return await destination.connect()

    @cog_ext.cog_slash(name="leave",description="leave vc", guild_ids=guild_ids)
    async def _leave(self, ctx:SlashContext):
        if not ctx.voice_client.is_playing:
            await ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send("leave")
        

    @cog_ext.cog_slash(name="skip", description="Skip a Song", guild_ids=guild_ids)
    async def _skip(self, ctx: SlashContext):
        if not ctx.voice_client.is_playing:
            return await ctx.send(con.Words.Skip.NOT_PLAYING)
        ctx.voice_client.stop()
        msg = await ctx.send(con.Words.Skip.SUCCESS)
        await msg.add_reaction(con.Emoji.SKIP)
        
    @cog_ext.cog_slash(name="pause", description="Pause the Song", guild_ids=guild_ids)
    async def _pause(self, ctx: SlashContext):
        if not ctx.voice_client.is_playing:
            return await ctx.send(con.Words.Pause.NOT_PLAYING)
        if ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
            ctx.voice_client.pause()
            msg = await ctx.send(con.Words.Pause.SUCCESS)
            await msg.add_reaction(con.Emoji.PAUSE_RESUME)

    @cog_ext.cog_slash(name="resume", description="Resume the Song", guild_ids=guild_ids)
    async def _resume(self, ctx: SlashContext):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            msg = await ctx.send(con.Words.Resume.SUCCESS)
            await msg.add_reaction(con.Emoji.PAUSE_RESUME)

    @cog_ext.cog_slash(name="queue", description="Show the Queue", guild_ids=guild_ids,options=[
            create_option(
                name="page", description="which page", required=False, option_type=10
            )
        ]
    )
    async def _queue(self, ctx: SlashContext, page=1):
        global Song_queue

        server_id = ctx.guild_id
        if not Song_queue[server_id] and not ctx.voice_client.is_playing():
            return await ctx.send(con.Words.Queue.EMPTY)
        
        items_per_page = 10
        pages = math.ceil((len(Song_queue[server_id]) + 1) / items_per_page)
        page = pages if page == -1 else min(max(1, page), pages)


        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ""
        for i, song in enumerate([ctx.voice_client.source] + Song_queue[server_id][start:end], start=start):
          if i == 0:
            queue += "[**{0.title}**]({0.url}){1}\n ------------\n".format(
               song, " <<< Now Playing"
          )
          else:
            queue += "`{0}.` [**{1.title}**]({1.url})\n".format(
                i , song
            )

        amount = len(Song_queue[server_id]) + 1 if self.loop[server_id] else len(Song_queue[server_id])
    
        

        embed = (
            discord.Embed(
                description=f"**{amount} Songs in Queue:{ con.Emoji.Loop.ON if self.loop[server_id] else '' }**\n\n{queue}", color=con.COLOR
            )
            .set_footer(text=f"Viewing page {page}/{pages}"))

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="loop", description="Loop!", guild_ids=guild_ids)
    async def _loop_queue(self, ctx: SlashContext):
        server_id = ctx.guild_id
        self.loop = self.loop if self.loop else {guild_id: loop for (
            guild_id, loop) in [(i.id, False) for i in self.bot.guilds]}
        if self.loop[server_id] == False:
            self.loop[server_id] = True
            msg = await ctx.send(con.Words.Loop.ON)
            await msg.add_reaction(con.Emoji.Loop.ON)
        else:
            self.loop[server_id] = False
            msg = await ctx.send(con.Words.Loop.OFF)
            await msg.add_reaction(con.Emoji.Loop.OFF)

    @cog_ext.cog_slash(
        name="play", description="Play some Music", guild_ids=guild_ids,
        options=[
            create_option(
                name="song",
                description="Song Name",
                required=True,
                option_type=3
            )
        ]
    )
    async def _play(self, ctx: SlashContext, *, song: str):
        global Song_queue

        await ctx.invoke(self._join)

        server_id = ctx.voice_client.server_id
        self.loop = self.loop if self.loop else {guild_id: loop for (
            guild_id, loop) in [(i.id, False) for i in self.bot.guilds]}

        await ctx.defer()
        source = await YTDLSource.create_source(ctx, song, loop=self.bot.loop)

        if server_id in Song_queue:
            Song_queue[server_id].append(source)
        else:
            Song_queue[server_id] = [source]
        if not ctx.voice_client.is_playing():
            self.song[server_id] = Song_queue[server_id].pop(0)
            ctx.voice_client.play(self.song[server_id], after=lambda e: asyncio.run(
                self.play_nexts_song(ctx)))

        song = Song(source)
        await ctx.send(embed=song.create_embed( con.Words.ENQUEUED))

    @cog_ext.cog_slash(
        name="remove", description="Remove Song from Queue", guild_ids=guild_ids,
        options=[
            create_option(
                name="index",
                description="Song Index to remove",
                required=True,
                option_type=10
            )
        ]
    )
    async def _remove(self, ctx: SlashContext, index: int):
        global Song_queue
        if not ctx.author.voice:
            return await ctx.send("no")
        server_id = ctx.guild_id
        if index == 0:
            msg = await ctx.send("Removed [**{0.title}**](<{0.url}>) 成功!".format(ctx.voice_client.source))
            self.song[server_id] = None
            ctx.voice_client.stop()
            return await msg.add_reaction("✅")
        if Song_queue[server_id] != []:
            index = min(max(index, -1), len(Song_queue[server_id]))  
            msg = await ctx.send("Removed {1} [**{0.title}**](<{0.url}>) 成功!".format(Song_queue[server_id].pop(index-1), index))
            return await msg.add_reaction("✅")
        else:
            return await ctx.send(con.Words.Queue.EMPTY)

    @cog_ext.cog_slash(name="now", description="Show Current Song", guild_ids=guild_ids)
    async def _now(self, ctx: commands.Context):
        await ctx.send(embed=Song(ctx.voice_client.source).create_embed(ctx.created_at))

    @cog_ext.cog_slash(name="clear", description="Clear the Queue", guild_ids=guild_ids)
    async def _clear(self, ctx: commands.Context):
        server_id = ctx.voice_client.server_id
        Song_queue[server_id] = []
        self.song[server_id] = None
        msg = await ctx.send(con.Words.Queue.CLEARED)
        await msg.add_reaction("✅")
