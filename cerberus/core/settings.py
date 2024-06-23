from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=False)

    # Main Vars

    OWNERS: List[int] = []
    DISCORD_TOKEN: str
    MAIN_COLOR: List[int] = [47, 49, 54]
    GUILDS: List[int] = []
    PROXY: Optional[str] = None
    PREFIX: List[str] = ","
    STRIP_AFTER_PREFIX: Optional[bool] = True

    # ModMail stuff
    
    MODMAIL_NOTIFICATIONS_CHANNEL: int
    MODMAIL_CHANNEL: int
    MODMAIL_WEBHOOK: str



settings = Settings()