import discord
from discord.ext import commands
import asyncio
import aiohttp
import io


class SteamMarket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def getitemprice(self, ctx: commands.context.Context, *, name: str, appid: int = 730):
        async with aiohttp.ClientSession() as session:
            url = f"http://127.0.0.1:8002/marketplace/{appid}?item={name}&fill=true&unquote=true"
            async with session.get(url) as resp:
                zamn = await resp.json()
        await ctx.send(zamn[-1]["value"])


async def setup(bot):
    await bot.add_cog(SteamMarket(bot))
