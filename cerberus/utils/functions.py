import ast as _ast
from datetime import datetime as _datetime

from disnake import Color as _Color
from disnake import Embed as _Embed


def create_error_embed(err : str) -> _Embed:
    err_embed = _Embed(title="We Got an Error!",
                              color=_Color.from_rgb(255, 3, 7),
                              description="⚠ "+str(err),
                              timestamp=_datetime.now())

    return err_embed

def chunker(text, chunk_size: int) -> list:
    length = len(text)
    num = 0
    chunks = []

    while num < len(text):
        chunks.append(text[num:length-(length-(chunk_size))+num:])
        num+=chunk_size

    return chunks

def insert_returns(body):
    # insert return stmt if the l_ast expression is an expression statement
    if isinstance(body[-1], _ast.Expr):
        body[-1] = _ast.Return(body[-1].value)
        _ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], _ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], _ast.With):
        insert_returns(body[-1].body)