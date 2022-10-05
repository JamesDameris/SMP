import discord
from discord.ext import commands
import asyncio
import aiohttp
import io
import traceback


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["rc"])
    @commands.is_owner()
    async def reloadcogs(self, ctx: commands.context.Context):
        s = ""
        for ext in self.bot.extensions.keys():
            await self.bot.reload_extension(ext)
            s += f":repeat:`{ext}`\n\n"
        await ctx.send(s)


async def setup(bot):
    await bot.add_cog(Utilities(bot))
