import os

import disnake
from disnake.ext import commands

from cerberus.core.client import Client
from cerberus.utils.database import DataBase
from cerberus.utils.env import Env

db = DataBase("./DataBase.db")
db.setup("main", "system", "channels")

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

async def setup_hook():
    pass


client = Client(intents=disnake.Intents.all(),
                allowed_mentions=disnake.AllowedMentions(replied_user=False),
                command_sync_flags=command_sync_flags,
                proxy=None,
                setup_hook=setup_hook)

client.load_extension("cogs.events.on_ready")


client.run(Env.get("TOKEN"))