import disnake

from cerberus.core.client import Client
from cerberus.core.settings import settings

client = Client(intents=disnake.Intents.all(),
                allowed_mentions=disnake.AllowedMentions(replied_user=False))

client.db.set("channels", "system", "main")


client.load_extension("cogs.events.on_ready")


client.run(settings.DISCORD_TOKEN)