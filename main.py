import os
import discord
from discord_slash import SlashCommand, SlashContext
from discord.ext import commands, tasks
from random import choice
from voice.music import Music
from voice.voiceslash import Vslash
from util.slashes import Slashes
from legacy.message import Yukinian
from env import TOKEN
from keepalive import keepalive


if __name__ == "__main__":

    bot = commands.Bot(command_prefix=commands.when_mentioned_or('IoIi '))
    slash = SlashCommand(bot, sync_commands = True)


    bot.add_cog(Music(bot))
    bot.add_cog(Vslash(bot))
    bot.add_cog(Slashes(bot))
    bot.add_cog(Yukinian(bot))
    

    @bot.event
    async def on_ready():
        print('ready!')
        change_status.start()

    
    @bot.event
    async def on_slash_command_error(ctx:SlashContext, ex):
        print('An error occurred: {}'.format(str(ex)))

  
    @tasks.loop(seconds=300)
    async def change_status():
        status: str = choice(['test', 'yes', 'no'])
        activity: discord.Activity = discord.Activity(
            type=discord.ActivityType.listening, name=status)
        await bot.change_presence(activity=activity)

    keepalive()
    bot.run(TOKEN)
