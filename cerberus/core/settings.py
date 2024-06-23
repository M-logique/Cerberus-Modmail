from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=False)

    # Main Vars

    OWNERS: list[ int ] = []
    DISCORD_TOKEN: str
    MAIN_COLOR: list[int] = [47, 49, 54]
    TEST_GUILDS: list[int] = []
    PROXY: str | None = None
    PREFIX: list[str] | str = ","
    STRIP_AFTER_PREFIX: bool | None = True

    # ModMail stuff
    
    MODMAIL_NOTIFICATIONS_CHANNEL: int
    MODMAIL_CHANNEL: int
    MODMAIL_WEBHOOK: str



settings = Settings()