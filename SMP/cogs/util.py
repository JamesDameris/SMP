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
        for ext in self.bot.extensions.keys():
            self.bot.reload_extension(ext)
            await ctx.send(f":repeat:{ext}")


async def setup(bot):
    await bot.add_cog(Utilities(bot))
