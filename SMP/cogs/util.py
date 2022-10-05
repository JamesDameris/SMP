import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import aiohttp
import io
import traceback


class Utilities(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="reloadcogs",
                          description="Reloads cogs (used for rapid development of commands without restarting bot")
    @commands.is_owner()
    async def reloadcogs(self, ctx: commands.context.Interaction):
        s = ""
        for ext in self.bot.extensions.keys():
            try:
                await self.bot.reload_extension(ext)
                s += f":repeat:`{ext}`\n\n"
            except Exception:
                s += f":x:`{ext}`]\n\n"
                raise
        await ctx.response.send_message(s, ephemeral=True)

    @commands.command(aliases=["scg"])
    @commands.is_owner()
    async def synccmdsguild(self, ctx: commands.context.Context, guildid: int = 1026974856597753976):
        self.bot.tree.copy_global_to(guild=discord.Object(id=1026974856597753976))
        await ctx.send("Done!")

    @commands.command()
    @commands.is_owner()
    async def syncall(self, ctx: commands.context.Context):
        await self.bot.tree.sync()
        await ctx.send("Done!")

async def setup(bot):
    await bot.add_cog(Utilities(bot))
