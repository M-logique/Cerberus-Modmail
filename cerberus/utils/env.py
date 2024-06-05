
from os import getenv as _getenv

from dotenv import load_dotenv as _load

# DEV Area !
_load()
_e = lambda e: _getenv(e)
_digit = lambda n: int(n) if n and n.isdigit() else n
# DEV Area !



class Env:
    """
    Class to receive some values from .env
    """


    @staticmethod
    def get(value: str) -> list | str | None:
        v = _e(value)

        if v is not None and "," in v:

            lst = [_digit(i.strip()) for i in v.split(",")]

            return lst
        
        return _digit(v)