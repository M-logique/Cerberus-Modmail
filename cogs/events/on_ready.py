import os

from disnake.ext import commands

from cerberus.utils.logger import logger


class OnReady(commands.Cog):
    
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        for folder in os.listdir('./cogs'):
            for filename in os.listdir(f"./cogs/{folder}"):
                if filename.endswith('.py'):
                    if filename[:-3] == "on_ready": continue
                    try:
                        self.client.load_extension(f'cogs.{folder}.{filename[:-3]}')
                        logger.info(f"loaded cogs.{folder}.{filename[:-3]}")
                    except Exception as e: 
                        logger.error(f"Error Loading cogs.{folder}.{filename[:-3]} - ", e)
        logger.info(f"Logged in as {self.client.user.display_name}")


def setup(client): client.add_cog(OnReady(client))