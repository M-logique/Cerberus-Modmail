import datetime

import disnake
from disnake.ext import commands
from requests import post

from cerberus.core.client import Client
from cerberus.core.settings import settings


def send(thread_id, message: disnake.Message): 

    payload = {
             "content": str(message.content)+"‌",
             "username": str(message.author.display_name),
             "avatar_url": str(message.author.avatar),
             "allowed_mentions": { "parse": [] }
         }
    url = settings.MODMAIL_CHANNEL
    params = {
        "thread_id": thread_id
    }
    r = post(url=url, 
         params=params,
         json=payload)
    
    return r

class OnDirectMessage(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        MAIN_COLOR = disnake.Color.from_rgb(*settings.MAIN_COLOR)
        db = self.client.db
        if message.guild == None and not message.author.bot: 
            i = db.get("%s-dm"%message.author.id, "channels")
            if not i:
                embed = disnake.Embed(title="new ticket from %s"% message.author,
                                    timestamp=datetime.datetime.now(),
                                    color=MAIN_COLOR)
                embed.set_footer(icon_url=message.author.avatar,
                                  text="New Ticket from %s"%message.author.id)

                desc = """**سلام وقت بخیر تیکت مادمیل شما ساخته شد. 
در صورت موفقیت ارسال پیام اموجی تایید زیر پیام شما ریکت می شود (:white_check_mark:) 
پیام شما در اسرع وقت توسط تیم ما جواب داده میشود ؛ با تشکر از همراهی شما.
**"""
                embed2 = disnake.Embed(title="تیکت شما با موفقیت ساخته شد.",
                                       description=desc,
                                       color=MAIN_COLOR,
                                       timestamp=datetime.datetime.now(),
                                       )

                button = disnake.ui.Button(style=disnake.ButtonStyle.secondary,
                                            emoji="🔒", 
                                            custom_id="close_this_shit",
                                            label="Close")
                
                channel = await self.client.fetch_channel(settings.MODMAIL_CHANNEL)
                thread = await channel.create_thread(
                        name="%s-ticket"% message.author,
                        auto_archive_duration=60,
                        embed=embed,
                        components = [button]
                    )
                await message.reply(embed = embed2)
                send(thread.thread.id, message)
                embed4 = disnake.Embed(title="🎫 New ModMail ticket",
                                       description="There is a new ModMail ticket who created by %s, **Click on the \"Claim\" Button for join**" % message.author,
                                       color=MAIN_COLOR,
                                       timestamp=datetime.datetime.now())
                
                add_button = disnake.ui.Button(style=disnake.ButtonStyle.success,
                                               label="Claim",
                                               custom_id="add_%s"%thread.thread.id,
                                               emoji="📨")
                
                notification_channels = await self.client.fetch_channel(settings.MODMAIL_NOTIFICATIONS_CHANNEL)
                await notification_channels.send(content="<@&1247524809697656976>",
                                                 embed=embed4,
                                                 components=add_button)
                if len(message.attachments) != 0:
                    attachments = [f"[{i.filename}]({i.url})" for i in message.attachments]

                    post(url="%s?thread_id=%s"%(settings.MODMAIL_WEBHOOK, i),
                        
                        json={
                            "content": str('\n'.join(attachments)),
                            "username": str(message.author.display_name),
                            "avatar_url": str(message.author.avatar),
                            "allowed_mentions": { "parse": [] }
                        })
                    
                await message.add_reaction("✅")
                db.set("%s-dm"%message.author.id, thread.thread.id, "channels")
                db.set("%s-mm"%thread.thread.id, message.author.id, "channels")
            else:

                r = send(i, message)
                if r.status_code == 400:
                    ch = db.get(f"{message.author.id}-dm", "channels")
                    db.delete(f"{message.author.id}-dm", "channels")
                    db.delete(f"{ch}-mm", "channels")

                            
                    return await message.add_reaction("❗")
                
                
                await message.add_reaction("✅")
                if len(message.attachments) != 0:
                    attachments = [f"[{i.filename}]({i.url})" for i in message.attachments]
                    post(url="%s?thread_id=%s"%(settings.MODMAIL_WEBHOOK, i),
                        
                        json={
                            "content": str('\n'.join(attachments)),
                            "username": str(message.author.display_name),
                            "avatar_url": str(message.author.avatar),
                            "allowed_mentions": { "parse": [] }
                        })
                    
        elif str(message.channel.type) == "public_thread":
            i = db.get("%s-mm"%message.channel.id, "channels")
            if i != None and i != "" and i != False:
                ch = await self.client.fetch_user(i)
                
                if not str(message.author.id) in settings.MODMAIL_WEBHOOK and not message.author.id == self.client.user.id:
                    try: 
                        await ch.send("%s‌"%(message.content))
                        await message.add_reaction("✅")
                        if len(message.attachments) != 0:
                            attachments = [f"[{i.filename}]({i.url})" for i in message.attachments]
                            await ch.send(content='\n'.join(attachments))
                    except Exception as err:
                        try: 
                            await message.add_reaction("❗")
                        except: pass


def setup(client):
    client.add_cog(OnDirectMessage(client))