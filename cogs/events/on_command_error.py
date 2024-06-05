from disnake.ext import commands

from cerberus.utils.functions import create_error_embed


class OnError(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingPermissions):
            text = "Sorry **{}**, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.reply(embed=create_error_embed(text))
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(embed=create_error_embed(f'This command is on cooldown, you can use it in {round(error.retry_after, 2)}s'))
        elif isinstance(error, commands.NotOwner):
            await ctx.reply(embed= create_error_embed("You are not owner"))
        else: 
            if len(str(error)) < 4000:
                await ctx.reply(embed=create_error_embed(str(error)))
            else:
                await ctx.reply(embed=create_error_embed(str(error)[:4000:]))

def setup(client: commands.Bot):
    client.add_cog(OnError(client))