from disnake import AllowedMentions as _AllowedMentions
from disnake import Intents as _Intents
from disnake.ext import commands as _commands

from ..utils.database import DataBase as _DataBase
from ..utils.logger import DiscordLogger as _Logger
from .settings import settings


class Client(_commands.Bot):
    """
    Modified discord client with some preset values
    """
    def __init__(self, intents: _Intents, 
                allowed_mentions: _AllowedMentions,
                **options):

        self.logger = _Logger("Cerberus-Modmail")
        self.db = _DataBase("./DataBase.db")


        test_guilds = settings.GUILDS
        owner_ids = settings.OWNERS
        prefix = settings.PREFIX
        proxy = settings.PROXY
        strip_aftre_prefix = settings.STRIP_AFTER_PREFIX



        super().__init__(command_prefix=_commands.when_mentioned_or(*prefix),
                         test_guilds=test_guilds,
                         owner_ids=owner_ids,
                         strip_after_prefix=strip_aftre_prefix,
                         allowed_mentions=allowed_mentions, 
                         intents=intents,
                         proxy=proxy,
                         help_command=None,
                         **options)


