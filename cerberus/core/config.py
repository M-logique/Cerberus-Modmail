import disnake as _disnake

from ..utils.env import Env as _Env

MODMAIL_WEBHOOK = _Env.get("MODMAIL_WEBHOOK")
MODMAIL_CHANNEL = _Env.get("MODMAIL_CHANNEL")
NOTIF_CHANNEL = _Env.get("MODMAIL_NOTIFICATIONS_CHANNEL")
MAIN_COLOR = _disnake.Color.red()
