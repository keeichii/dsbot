#discord bot by @keeichii
import disnake
from disnake import MessageInteraction
from disnake.ext import commands
from typing import Optional

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    help_command=None,
    intents=disnake.Intents.all(),
    test_guilds=[1283143632416800853]
)

CENSORED_WORDS = ['тупой']



#events

@bot.event
async def on_member_join(member):
    role = await disnake.utils.get(
        member.guild.roles,
        id=1283150328711090368
    )

    channel = bot.get_channel(1283143633024978947)
    #channel = member.guild.system_channel

    embed = disnake.Embed(
        title='новый чел',
        description=f'{member.name}#{member.discriminator}',
        color=0xfffff
    )

    await member.add_roles(role)
    await channel.send(embed=embed)


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    for content in message.content.split():
        for censored_word in CENSORED_WORDS:
            if content.lower() == censored_word:
                await message.delete()
                await message.channel.send(f'{message.author.mention} айайай')


@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author} недостаточно прав емае')

    elif isinstance(error, commands.UserInputError):
        await ctx.send(
            embed=disnake.Embed(
                description=f'правильно: `{ctx.prefix}{ctx.command.name}` ({ctx.command.bried})\n пример для тупых: {ctx.prefix}{ctx.command.usage}'
            )
        )


#commands

@bot.command(usage='kick <@user> <reason=None>')
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: disnake.Member, *, reason='новый год епта'):
    await ctx.send(f'{ctx.author.mention} выкинул нахуй за борт {member.mention}', delete_after=60)
    await member.kick(reason=reason)
    await ctx.message.delete()


@bot.command(name='бан', aliases=['баня', 'банан'], usage='ban <@user> <reason=None>')
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: disnake.Member, *, reason='новый год епта'):
    await ctx.send(f'{ctx.author.mention} выкинул нахуй за борт {member.mention}', delete_after=60)
    await member.ban(reason=reason)
    await ctx.message.delete()


@bot.command(usage='muted <@user>')
@commands.has_permissions(administrator=True)
async def muted(member):
    role_m = await disnake.utils.get(
        member.guild.roles,
        id=1283158223804829837
    )
    await member.add_roles(role_m)


@bot.command(usage='unmuted <@user>')
@commands.has_permissions(administrator=True)
async def unmuted(member):
    role_um = await disnake.utils.get(
        member.guild.roles,
        id=1283150328711090368
    )
    await member.add_roles(role_um)


@bot.command(name='party')
async def ask_party(ctx):
    view = Confirm()

    await ctx.send('приглос', view=view)
    await view.wait()

    if view.value is None:
        await ctx.send('опоздал')
    elif view.value:
        await ctx.send('лови', view=LinkToParty())
    else:
        await ctx.send('не')


@bot.command()
async def order(ctx):
    await ctx.send('выбирай', view=DropdownView())


@bot.slash_command(description='калькулятор для отсталых')
async def calc(inter, a: int, oper: str, b: int):
    if oper == '+':
        result = a + b
    elif oper == '-':
        result = a - b
    elif oper == '*':
        result = a * b
    elif oper == '/':
        result = a / b
    elif oper == '//':
        result = a // b
    elif oper == '%':
        result = a % b
    elif oper == '**':
        result = a ** b
    else:
        result = 'э'

    await inter.send(str(result))



#buttons

class Confirm(disnake.ui.View):

    def __init__(self):
        super().__init__(timeout=10.0)
        self.value = Optional[bool]

    @disnake.ui.button(label='confirm', style=disnake.ButtonStyle.green, emoji='😊')
    async def confirm(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_message('жди')
        self.value = True
        self.stop()

    @disnake.ui.button(label='cancel', style=disnake.ButtonStyle.red, emoji='🙁')
    async def cancel(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_message('пон(')
        self.value = False
        self.stop()

    @disnake.ui.button(label='thinkin`', style=disnake.ButtonStyle.blurple, emoji='🤔')
    async def cancel(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_message('пон(')
        self.value = False
        self.stop()


class LinkToParty(disnake.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(label='фоллоу', url='https://vk.com/keeichi'))



class Dropdown(disnake.ui.StringSelect):

    def __init__(self):
        options = [
            disnake.SelectOption(label='sisi', description='епта'),
            disnake.SelectOption(label='pizda', description='епта'),
            disnake.SelectOption(label='hui', description='епта')
        ]

        super().__init__(
            placeholder='MENU',
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, inter: disnake.MessageInteraction):
        await inter.response.send_message(f'предпочтение: {self.values[0]}')


class DropdownView(disnake.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())



'''
if __name__ == '__main__':
    main()
'''

@bot.event
async def on_ready():
    print(f'{bot.user} is alive.')

bot.run('ds bot token')