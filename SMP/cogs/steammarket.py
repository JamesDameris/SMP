import typing

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
from discord import app_commands
from tabulate import tabulate

from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
pd.plotting.plot_params = {'x_compat': True}


class SteamMarket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="getitemprice", description="Get historical item prices for an item")
    async def getitemprice(self, ctx: discord.Interaction, *, name: str, wear: typing.Optional[typing.Literal[
        "Minimal Wear", "Factory New", "Battle-Scarred", "Well-Worn", "Field-Tested"
    ]] = None, appid: int = 730):
        async with aiohttp.ClientSession() as session:
            url = f"http://127.0.0.1:8002/marketplace/{appid}?item=" \
                  f"{urllib.parse.quote_plus(name+wear if wear is not None else name)}" \
                  f"&fill=true&unquote=true"
            async with session.get(url) as resp:
                zamn = await resp.json()
        if "error" in zamn:
            await ctx.response.send_message(f"Cannot find price for {name}. l + ratio + skill issue")
            return
        df = pd.DataFrame([(str(i["date"]), float(i["value"])) for i in zamn], columns=["Date", "Price"])
        df["Date"] = pd.to_datetime(df["Date"])
        ax = sns.lineplot(data=df, x="Date", y="Price")
        ax.set(title="Price vs Time", ylabel="Price ($)")
        plt.xticks(rotation=20)
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())

        # plt.show()
        stream = io.BytesIO()
        plt.savefig(stream, format="png")
        stream.seek(0)
        ax.clear()
        embed = discord.Embed(color=0x00CFFF, title=f"Data for {name}")
        embed.set_image(url=f"attachment://graph.png")
        embed.add_field(name="Current Price", value=zamn[-1]['value'])
        table = tabulate([[x["value"]] for x in zamn[-7:]], tablefmt="grid",
                         showindex=[x["date"] for x in zamn[-7:]])
        embed.add_field(name="Recent History", value=table, inline=False)
        await ctx.response.send_message(file=discord.File(stream, filename=f"graph.png"), embed=embed)


async def setup(bot):
    await bot.add_cog(SteamMarket(bot))

def wearParser(wear):
    if wear == "":
        return wear
    sWear = ""
    if " " in wear:
        sWear = wear.split(" ")
        wear = sWear[0] + sWear[1]

    elif "-" in wear:
        sWear = wear.split("-")
        wear = sWear[0] + sWear[1]

    wear = wear.lower()

    if wear == "minimalwear":
        wear = "(Minimal Wear)"
    elif wear == "factorynew":
        wear = "(Factory New)"
    elif wear == "battlescarred":
        wear = "(Battle-Scarred)"
    elif wear == "wellworn":
        wear = "(Well-Worn)"
    elif wear == "fieldtested":
        wear = "(Field-Tested)"
    return wear