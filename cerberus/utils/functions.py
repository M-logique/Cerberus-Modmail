from datetime import datetime as _datetime

from disnake import Color as _Color
from disnake import Embed as _Embed


def create_error_embed(err : str) -> _Embed:
    err_embed = _Embed(title="We Got an Error!",
                              color=_Color.from_rgb(255, 3, 7),
                              description="⚠ "+str(err),
                              timestamp=_datetime.now())

    return err_embed