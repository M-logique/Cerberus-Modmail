import disnake
from disnake.ext import commands
from requests import post

from cerberus.core.client import Client
from cerberus.core.settings import settings
from cerberus.utils.functions import create_error_embed

MODMAIL_WEBHOOK = settings.MODMAIL_WEBHOOK
MODMAIL_CHANNEL = settings.MODMAIL_CHANNEL
NOTIF_CHANNEL = settings.MODMAIL_NOTIFICATIONS_CHANNEL



class OnButtonClick(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        custom_id = inter.component.custom_id
        db = self.client.db
        if custom_id == "close_this_shit":
            await inter.response.send_message("🔒 **This ticket was closed by `%s`**" % inter.author)
            user = db.get("%s-mm"%inter.channel.id, "channels")
            db.delete("%s-dm"%user, "channels")
            db.delete("%s-mm"%inter.channel.id, "channels")
            u = await self.client.fetch_user(user)
            await u.send("🔒 **Your ticket was closed by `%s`** "%inter.author)
            await inter.message.edit(components=None)
            await inter.channel.edit(archived=True)
        elif "add_" in custom_id:
            thread_id = custom_id.split("_")[1]
            channel = await self.client.fetch_channel(MODMAIL_CHANNEL)
            thread = channel.get_thread(int(thread_id))

            if not thread == None and not inter.author.id in [i.id for i in thread.members]:
                try:
                    await thread.add_user(disnake.Object(id=inter.author.id))
                    await inter.response.send_message(content="✅ Done - <#%s>" % thread_id, 
                                                      ephemeral=True)
                except Exception as err: await inter.response.send_message(content="❗ There was a problem", 
                                                          ephemeral=True,
                                                          embed=create_error_embed(str(err)))
            elif thread == None:
                await inter.response.send_message(content="🤔 This thread isn't exists any more",
                                                  ephemeral=True)
            else:
                await inter.response.send_message(content="❓ You are aleardy in",
                                                  ephemeral=True)




def setup(client):
    client.add_cog(OnButtonClick(client))