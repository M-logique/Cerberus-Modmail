import ast
import datetime
import os

import disnake
from disnake.ext import commands

from cerberus.core.config import MAIN_COLOR
from cerberus.utils.functions import chunker, insert_returns


class Buttons(disnake.ui.View):
    def __init__(self, author, chunk) -> None:

        super().__init__(timeout=180)
        super().add_item(self.SexButtons(author=author, label="<<<", chunk=chunk))
        super().add_item(self.SexButtons(author=author, label=">>>", chunk=chunk))
    class SexButtons(disnake.ui.Button):  # Button class
        def __init__(self, label, author, chunk):
            self.chunk, self.author = chunk, author
            self.index = 0
            super().__init__(label=label, style=disnake.ButtonStyle.secondary)  # set label and super init class

        async def callback(self, interaction: disnake.MessageInteraction):
            if interaction.author.id != self.author: return await interaction.response.send_message(content="This is not yours", ephemeral=True)
            if interaction.component.label == ">>>":
                if self.index == len(self.chunk)-1:
                    self.index = 0
                else:
                    self.index+=1
                    
                embed = disnake.Embed(description=self.chunk[self.index],
                                        color=MAIN_COLOR,
                                        timestamp=datetime.datetime.now())
                embed.set_footer(text="Page %s/%s" % (self.index+1, len(self.chunk)), icon_url=interaction.author.avatar)
                await interaction.response.edit_message(embed=embed)
            elif interaction.component.label == "<<<":
                if self.index == 0:
                    self.index = len(self.chunk)-1
                else:
                    self.index-=1
                embed = disnake.Embed(description=self.chunk[self.index],
                                        color=MAIN_COLOR,
                                        timestamp=datetime.datetime.now())
                embed.set_footer(text="Page %s/%s" % (self.index+1, len(self.chunk)), icon_url=interaction.author.avatar)
                await interaction.response.edit_message(embed=embed)



class DevCommands(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command(name="eval", aliases=["e"],
                      usage="<Code>",
                      description= "Evals some codes")
    @commands.is_owner()
    async def _eval(self, ctx: commands.Context, *, code: str = "Kir"):
        fn_name = "_eval_expr"
        cmd = code.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)
        env = {
            'client': ctx.bot,
            'disnake': disnake,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = str((await eval(f"{fn_name}()", env)))
        if result != "None":
            if len(result) < 4000:
                await ctx.send(embed=disnake.Embed(color=MAIN_COLOR, description=result, title="Evaluation result", timestamp=datetime.datetime.now()))
            else:
                chunks = chunker(result, chunk_size=4000)
                embed = disnake.Embed(description=chunks[0],
                                        color=MAIN_COLOR,
                                        timestamp=datetime.datetime.now())
                embed.set_footer(text="Page %s/%s" % (1, len(chunks)), icon_url=ctx.author.avatar)

                await ctx.send(view=Buttons(author=ctx.author.id, chunk=chunks), embed=embed)
        else:
            await ctx.send(embed=disnake.Embed(description="*There is no Evaluation result*", timestamp=datetime.datetime.now(), color=MAIN_COLOR))




    @commands.command(name="reload", aliases=["load"],
                    usage="",
                    description= "Will Reload Commands without restart",)
    @commands.is_owner()
    async def _reload(self, ctx):
        loaded = []
        for folder in os.listdir('./Cogs'):
                if folder == "tasks": continue
                for filename in os.listdir(f"./Cogs/{folder}"):
                    if filename.endswith('.py'):
                        try: self.client.unload_extension(f'Cogs.{folder}.{filename[:-3]}')
                        except: pass
                        try:self.client.load_extension(f'Cogs.{folder}.{filename[:-3]}')
                        except: pass
                        loaded.append(f"Cogs.{folder}.{filename[:-3]}")
        else:
            embed = disnake.Embed(title="Load Successful",
                                description="%s Cogs Loaded: \n```%s```" % (len(loaded),",\n".join(loaded)),
                                color=MAIN_COLOR,
                                timestamp=datetime.datetime.now())
            await ctx.reply(embed=embed)

        





def setup(client: commands.Bot):
    client.add_cog(DevCommands(client))