import logging
import traceback

import aiohttp
import discord
from discord.ext.commands import *
from jishaku.help_command import *
import io
import asyncio
import os
import base64 as b64

intents = discord.Intents.all()
print(intents)


class SIMP(Bot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(prefix, *args, **kwargs)
        self.invite = None

    async def on_connect(self):
        pass

    async def on_ready(self):
        self.invite = "https://discord.com/api/oauth2/authorize?client_id=1026972340933894234&permissions=8&scope=applications.commands%20bot"
        print(
            "Logged in as",
            client.user.name,
            "\nId:",
            client.user.id,
            "\nOath:",
            self.invite,
        )
        print("--------")
        self.ogerror = self.tree.on_error
        self.tree.on_error = self.on_app_command_error

    async def on_message(self, msg: discord.Message):
        # ctx = await self.get_context(msg)
        try:
            await self.process_commands(msg)
        except Exception as err:
            print(err)

    async def logout(self):
        await super().logout()

    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    async def on_app_command_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        print(interaction.type)
        logging.getLogger("discord").error(traceback.format_exc())
        if interaction.type == discord.InteractionType.ping:
            # WHAT THE ACTUAL FUCK THIS SHOULDNT HAPPEN
            await self.logout()
        elif interaction.type == discord.InteractionType.application_command and interaction.response.type is None:
            await interaction.response.send_message(traceback.format_exc())
        elif interaction.type == discord.InteractionType.application_command and interaction.response.type == discord.InteractionResponseType.channel_message:
            await interaction.channel.send(traceback.format_exc())
        elif interaction.type == discord.InteractionType.application_command:
            await interaction.followup.send(traceback.format_exc())
        else:
            await interaction.channel.send(f"Error! {traceback.format_exc()}")

    async def process_commands(self, message):
        await super().process_commands(message)

    async def playingstatus(self):
        await self.wait_until_ready()
        while self.is_ready():
            status = "with viruses"
            await self.change_presence(
                activity=discord.Game(name=status), status=discord.Status.online
            )
            await asyncio.sleep(120)

    async def setup_hook(self):
        nocogs = []
        for file in os.listdir("cogs"):
            if file.endswith(".py") and not (file[:-3] in nocogs):
                name = file[:-3]
                try:
                    await client.load_extension(f"cogs.{name}")
                    print(f"Loaded cog {name}")
                except Exception as e:
                    print(f"Failed to load cog {name} due to error\n", e)
        await client.load_extension("jishaku")


client = SIMP(
    intents=intents, prefix=when_mentioned_or("!"), help_command=DefaultPaginatorHelp()
)

try:
    with open("token.txt") as f:
        client.run(f.read().replace("\n", "").replace("\r", ""))
except FileNotFoundError:
    print("create token.txt")
except:
    print("Bye!")
    raise
