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
                command_sync_flags: _commands.CommandSyncFlags):

        prefix = _E.get("PREFIX")
        guilds = _E.get("GUILDS")
        owners = _E.get("OWNERS")
        proxy = _E.get("PROXY")
        strip_aftre_prefix = _E.get("STRIP_AFTER_PREFIX")
        

        self.setup_hook = setup_hook

        test_guilds = None
        owner_ids, owner_id = (None, )*2
        

        if isinstance(prefix, list): 
            prefix = _commands.when_mentioned_or(*prefix)
        
        else:
            prefix = _commands.when_mentioned_or(prefix)

        if isinstance(guilds, list):
            test_guilds = guilds
        elif isinstance(guilds, int):
            test_guilds = [guilds]
        
        if isinstance(owners, list):
            owner_ids = owners
        elif isinstance(owners, int):
            owner_id = owners


        super().__init__(command_prefix=prefix,
                         test_guilds=test_guilds,
                         owner_ids=owner_ids,
                         owner_id=owner_id,
                         strip_after_prefix=bool(strip_aftre_prefix),
                         allowed_mentions=allowed_mentions, 
                         intents=intents,
                         command_sync_flags=command_sync_flags,
                         proxy=proxy,
                         help_command=None,
                         )
        
    async def setup_hook(self):

        await self.setup_hook()
        

