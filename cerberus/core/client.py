from typing import Any

from disnake import AllowedMentions as _AllowedMentions
from disnake import Intents as _Intents
from disnake.ext import commands as _commands

from ..utils.env import Env as _E


class Client(_commands.Bot):
    """
    Modified discord client with some preset values
    """
    def __init__(self, intents: _Intents, 
                allowed_mentions: _AllowedMentions,
                setup_hook: Any,
                command_sync_flags: _commands.CommandSyncFlags,
                proxy: str):

        prefix = _E.get("PREFIX")
        guilds = _E.get("GUILDS")
        owners = _E.get("OWNERS")
        strip_aftre_prefix = _E.get("STRIP_AFTER_PREFIX")
        

        self.setup_hook = setup_hook

        if isinstance(prefix, list): 
            prefix = _commands.when_mentioned_or(*prefix)
        
        else:
            prefix = _commands.when_mentioned_or(prefix)

        super().__init__(command_prefix=prefix,
                         test_guilds=guilds,
                         owner_ids=owners,
                         strip_after_prefix=bool(strip_aftre_prefix),
                         allowed_mentions=allowed_mentions, 
                         intents=intents,
                         command_sync_flags=command_sync_flags,
                         proxy=proxy,
                         help_command=None)
        
    async def setup_hook(self):

        await self.setup_hook()
        

