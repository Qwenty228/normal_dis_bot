from discord import utils
from discord.ext import commands
import discord
import random, math
import datetime




class Yukinian(commands.Cog):
    """She is cute, isn't she"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.Cog.listener()
    async def on_message(self, message):        
        if message.author == self.bot.user:
            return
        if "1857"  in message.content:
            a = bool(random.randint(0, 2))
            if a:
                embed = (discord.Embed(title="***HORNIPEDIA***", description= "There's still lots of work that needs to be done, Doctor. You can't rest now! ", color=0xF93F17)  # discord.Color.blurple())
                    .set_image(url="https://cdn.discordapp.com/attachments/889528076646617128/910542492951261254/82782768_p0.png")
                    .set_footer(text="mikkuhoruni", icon_url=message.author.avatar_url))
                await message.channel.send("https://media.discordapp.net/attachments/889528076646617128/909654746640576562/horuni.gif")
            else:
                embed = (discord.Embed(title="Mlkipedia", description= "Big sister Amiya is really amazing. She always has so many ideas that I haven't thought of, and she's a great role model. But, she's also just like me. She's not an adult yet, so she'll sometimes feel lost and confused. Doctor, you should spend more time with her.", color=0xF93F17)  # discord.Color.blurple())
                    .set_image(url="https://i.redd.it/xhq0uiq2a4461.gif")
                    .set_footer(text="caffe latte caffe mocca cappuccino", icon_url=message.author.avatar_url))
            await message.channel.send(embed=embed)


            # message.channel.send(random.choice(word_choices))
        
   

    @commands.command(name='none', aliases=['n'])
    async def none(self, ctx):
        """cum"""
        await ctx.send("cum")
    
    