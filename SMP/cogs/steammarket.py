import discord
from discord.ext import commands
import asyncio
import aiohttp
import io
import urllib.parse
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
pd.plotting.plot_params = {'x_compat': True}

class SteamMarket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["gip"])
    @commands.is_owner()
    async def getitemprice(self, ctx: commands.context.Context, *, name: str, appid: int = 730):
        async with aiohttp.ClientSession() as session:
            url = f"http://127.0.0.1:8002/marketplace/{appid}?item={urllib.parse.quote_plus(name)}&fill=true&unquote=true"
            async with session.get(url) as resp:
                zamn = await resp.json()
        df = pd.DataFrame([(str(i["date"]), float(i["value"])) for i in zamn], columns=["Date", "Price"])
        df["Date"] = pd.to_datetime(df["Date"])
        ax = sns.lineplot(data=df, x="Date", y="Price")
        ax.set(title="Price vs Time")
        plt.xticks(rotation=20)
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())

        # plt.show()
        plt.savefig("tempfigs\\tmfig.png")
        ax.clear()
        await ctx.send(f"Latest price: ${zamn[-1]['value']}", file=discord.File('tempfigs\\tmfig.png'))


async def setup(bot):
    await bot.add_cog(SteamMarket(bot))
