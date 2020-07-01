import discord
from discord.ext import commands
from discord.utils import get
import asyncio

import sqlite3

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

bot_version = 'v1.0.5'
PREFIX = '.'
client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )

@client.event
async def on_command_error( ctx, error ):
    pass

@client.event
async def on_ready():
    await client.change_presence( status = discord.Status.online, activity = discord.Game( '{}help'.format( PREFIX ) ) )

    cursor.execute( """CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT,
        cash BIGINT,
        rep INT,
        lvl INT
    )""" )

    cursor.execute( """CREATE TABLE IF NOT EXISTS shop (
        role_id INT,
        id INT,
        cost BIGINT
    )""" )

    for guild in client.guilds:
        for member in guild.members:
            if cursor.execute( f'SELECT id FROM users WHERE id = { member.id }' ).fetchone() is None:
                cursor.execute( f'INSERT INTO users VALUES ("{ member }", { member.id }, 0, 0, 1)' )
            else:
                pass

    connection.commit()
    print( f'Bot connected { bot_version }' )



#Переменные
TOKEN = 'NzI0OTY3NjMxNDcxMzc4NDg0.Xvh6Vg.zOsKJF549-oxks2LdTrgG74y7y4'
ID = 724967631471378484

id_connect_server = 482502913743257600 #Канал для отображения присоединения на сервер

role_squad = 607888007315587092
role_moder = 482272417549516800
role_banned = 727225785332662293
role_muted = 727225716399276033

insufficient_rights_error = discord.Embed( description = 'У вас недостаточно прав на выполнение этой команды!', colour = discord.Color.red() )
bad_words = [ 'тест' ]

color_ban = 0xff0000 #red
color_warn = 0xffff00 #yelow
color_kick = 0x0080ff #blue
color_main = 0xff8000 #orange
color_unban = 0x00ff00 #green
color_kus = 0x00ffff



#Очистка сообщений
@client.command( aliases = [ 'clear', 'очистить' ] )
@commands.has_permissions( administrator = True )

async def __clear( ctx, amount = 1 ):
    await ctx.channel.purge( limit = amount+1 )

    await ctx.send( embed = discord.Embed( description = f':white_check_mark: Удалено { amount } сообщений', colour = discord.Color.green() ), delete_after = 1 )

@__clear.error
async def clear_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )



#Кик
@client.command( aliases = [ 'kick', 'кикнуть', 'кик' ] )
@commands.has_permissions( administrator = True )

async def __kick( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )

    if reason == None:
        await ctx.send( embed = discord.Embed( description = f'{ ctx.message.author.mention }, обязательно укажи причину!', colour = discord.Color.red() ), delete_after = 5 )
        return

    if member == None or member == ctx.message.author:
        await ctx.send( embed = discord.Embed( description = f'{ member.mention }, вы не можете кикнуть самого себя', colour = discord.Color.red() ), delete_after = 5 )
        return

    await member.send( embed = discord.Embed( description = f'Вы были исключены из **Foren Server** администратором **{ ctx.author.mention }** ```Причина: { reason }```', color = color_kick ) )

    await member.kick( reason = reason )

    embed = discord.Embed( color = color_kick )
    embed.set_author( name = member.name, icon_url = member.avatar_url )
    embed.add_field( name = "Пользователь", value = format( member.mention ), inline = False )
    embed.add_field( name = "Администратор", value = format( ctx.message.author.mention ), inline = False )
    embed.add_field( name = "Причина", value = reason, inline = False )
    embed.set_footer( text= f"Исключён администратором { ctx.author.name }", icon_url = ctx.author.avatar_url )

    await ctx.send( embed = embed )

@__kick.error
async def kick_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}kick [@участник] (причина) - кикнуть с сервера```'.format( PREFIX ), delete_after = 5 )



#Бан
@client.command( aliases = [ 'ban', 'бан', 'забанить' ] )
@commands.has_permissions( administrator = True )

async def __ban( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )

    if reason == None:
        await ctx.send( embed = discord.Embed( description = f'{ ctx.author.name }, обязательно укажи причину!', colour = discord.Color.red() ), delete_after = 5 )
        return

    if member == None or member == ctx.message.author:
        await ctx.send( embed = discord.Embed( description = f'{ member.mention }, вы не можете заблокировать самого себя', colour = discord.Color.red() ), delete_after = 5 )
        return

    await member.ban( reason = reason )

    await member.send( embed = discord.Embed( description = f'Вы были заблокированы на **Foren Server** администратором **{ ctx.author.mention }** ```Причина: { reason }```', color = color_ban ) )

    embed = discord.Embed( color = color_ban )
    embed.set_author( name = member.name, icon_url = member.avatar_url )
    embed.add_field( name = "Пользователь", value = format( member.mention ), inline = False )
    embed.add_field( name = "Администратор", value = format( ctx.message.author.mention ), inline = False )
    embed.add_field( name = "Причина", value = reason, inline = False )
    embed.add_field( name = "Длительность", value = "∞", inline = False )
    embed.set_footer( text= f"Заблокирован администратором { ctx.author.name }", icon_url = ctx.author.avatar_url )

    await ctx.send( embed = embed )

@__ban.error
async def ban_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}ban [@участник] (причина) - забанить навсегда```'.format( PREFIX ), delete_after = 5 )


#Разбан
@client.command( aliases = [ 'unban', 'унбан', 'анбан', 'разбанить' ] )
@commands.has_permissions( administrator = True )

async def __unban( ctx, *, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )

    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban( user )

        await ctx.send( f'Разбанен { user.mention }' )

        embed = discord.Embed( color = color_unban )
        embed.set_author( name = member.name, icon_url = member.avatar_url )
        embed.add_field( name = "Пользователь", value = format( member.mention ), inline = False )
        embed.add_field( name = "Администратор", value = format( ctx.message.author.mention ), inline = False )
        embed.set_footer( text= f"Был разбанен администратором { ctx.author.name }", icon_url = ctx.author.avatar_url )

        await ctx.send( embed = embed )

        return

@__unban.error
async def unban_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}unban [участник#0000] - разбанить```'.format( PREFIX ), delete_after = 5 )



#Предупреждение
@client.command( aliases = [ 'warn', 'варн', 'предупредить' ] )
@commands.has_permissions( administrator = True )

async def __warn( ctx, member: discord.Member, *, reason ):
    await ctx.channel.purge( limit = 1 )

    if member == None or member == ctx.message.author:
        await ctx.send( embed = discord.Embed( description = f'{ member.mention }, вы не можете предупредить самого себя', colour = discord.Color.red() ), delete_after = 5 )
        return

    await ctx.sent( embed = discord.Embed( description = f'{ member.mention } вы были предупреждены ```Причина: { reason }```', color = color_warn ) )

    await member.send( embed = discord.Embed( description = f'Вы были предупреждены на **Foren Server** администратором **{ ctx.author.mention }** ```Причина: { reason }```', color = color_warn ) )

    #embed = discord.Embed( color = color_warn )
    #embed.set_author( name = member.name, icon_url = member.avatar_url )
    #embed.add_field( name = "Пользователь", value = format( member.mention ), inline = False )
    #embed.add_field( name = "Модератор", value = format( ctx.author.name ), inline = False )
    #embed.add_field( name = "Причина", value = reason, inline = False )
    #embed.set_footer( text= f"Был предупреждён администратором { ctx.author.name }", icon_url = ctx.author.avatar_url )

    #await ctx.send( embed = embed )

@__warn.error
async def warn_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}warn [@участник] (причина) - предупредить```'.format( PREFIX ), delete_after = 5 )



#Временный бан
@client.command( aliases = [ 'tempban', 'темпбан', 'временныйбан' ] )
@commands.has_permissions( administrator = True )

async def __tempban( ctx, member: discord.Member, time: int, *, reason ):
    await ctx.channel.purge( limit = 1 )

    if member == None or member == ctx.message.author:
        await ctx.send( embed = discord.Embed( description = f'{ member.mention }, вы не можете забанить самого себя', colour = discord.Color.red() ), delete_after = 5 )
        return

    if time == None or 0:
        await ctx.send( embed = discord.Embed( description = f'{ ctx.message.author.mention }, обязательно укажи время!', colour = discord.Color.red() ), delete_after = 5 )
        return

    if reason == None:
        await ctx.send( embed = discord.Embed( description = f'{ ctx.message.author.mention }, обязательно укажи причину!', colour = discord.Color.red() ), delete_after = 5 )
        return

    await member.add_roles( discord.utils.get( ctx.message.guild.roles, id = role_banned ) )

    embed = discord.Embed( description = f'Пользователь { member.mention } был временно заблокирован за нарушение прав! ```Длительность: { time } минут(а)``` ```Причина: { reason }```', color = color_ban )
    embed.set_footer( text = f"Заблокирован администратором { ctx.author.name }", icon_url = ctx.author.avatar_url )
    await ctx.send( embed = embed )

    await member.send( embed = discord.Embed( description = f'Вы были заблокированы на **Foren Server** ```Длительность: { time } минут(а)``` ```Причина: { reason }```', color = color_ban ) )

    await asyncio.sleep( time * 60 )

    await member.remove_roles( discord.utils.get( ctx.message.guild.roles, id = role_banned ) )

    await ctx.send( embed = discord.Embed( description = f'Пользователь { member.mention } разбанен по истечению времени', color = color_unban ) )

    await member.send( embed = discord.Embed( description = 'Вы были разбанены по истечению времени', color = color_unban ) )

@__tempban.error
async def tempban_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}tempban [@участник] (время в минутах) (причина) - забанить```'.format( PREFIX ), delete_after = 5 )



#Мут
@client.command( aliases = [ 'mute', 'мут', 'заглушить', 'замутить' ] )
@commands.has_permissions( administrator = True )

async def __mute( ctx, member: discord.Member, time: int, *, reason ):
    await ctx.channel.purge( limit = 1 )

    if member == None or member == ctx.message.author:
        await ctx.send( embed = discord.Embed( description = f'{ member.mention }, вы не можете заглушить самого себя', colour = discord.Color.red() ), delete_after = 5 )
        return

    if time == None or 0:
        await ctx.send( embed = discord.Embed( description = f'{ ctx.message.author.mention }, обязательно укажи время!', colour = discord.Color.red() ), delete_after = 5 )
        return

    if reason == None:
        await ctx.send( embed = discord.Embed( description = f'{ ctx.message.author.mention }, обязательно укажи причину!', colour = discord.Color.red() ), delete_after = 5 )
        return

    await member.add_roles( discord.utils.get( ctx.message.guild.roles, id = role_muted ) )

    embed = discord.Embed( description = f'У { member.mention } ограничение чата за нарушение прав! ```Длительность: { time } минут(а)``` ```Причина: { reason }```', color = color_ban )
    embed.set_footer( text= f"Заглушен администратором { ctx.author.name }", icon_url = ctx.author.avatar_url )
    await ctx.send( embed = embed )

    await member.send( embed = discord.Embed( description = f'У вас ограничение чата на **Foren Server** ```Длительность: { time } минут(а)``` ```Причина: { reason }```', color = color_ban ) )

    await member.move_to( None ) #Когда мутят он дисконектится

    await asyncio.sleep( time * 60 )

    await member.remove_roles( discord.utils.get( ctx.message.guild.roles, id = role_muted ) )

    await ctx.send( embed = discord.Embed( description = f'У { member.mention } снято ограничение чата по истечению времени', color = color_unban ) )

    await member.send( embed = discord.Embed( description = 'У вас снято ограничение чата по истечению времени', color = color_unban ) )

@__mute.error
async def mute_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}mute [@участник] (время в минутах) (причина) - заглушить```'.format( PREFIX ), delete_after = 5 )



#Размут
@client.command( aliases = [ 'unmute', 'разглушить', 'унмут', 'анмут', 'размут', 'размутить' ] )
@commands.has_permissions( administrator = True )

async def __unmute( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )

    await member.remove_roles( discord.utils.get( ctx.message.guild.roles, id = role_muted ) )

    embed = discord.Embed( description = f'У { member.mention } снят мут', color = color_unban )
    embed.set_footer( text= f"Размучен администратором { ctx.author.name }", icon_url = ctx.author.avatar_url )
    await ctx.send( embed = embed )

    await member.send( embed = discord.Embed( description = f'У вас снято ограничение чата администратором { ctx.author.name }', color = color_unban ) )

@__unmute.error
async def unmute_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}unmute [@участник] - размутить```'.format( PREFIX ), delete_after = 5 )



#Бот который кусает и целует
@client.command( aliases = [ 'кусь', 'укусить', 'куснуть' ] )

async def __ukus( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )

    if member == None or member == ctx.message.author:
        await ctx.send( embed = discord.Embed( description = f'{ member.mention } укусил(а) себя', color = color_kus ) )
        return

    await ctx.send( embed = discord.Embed( description = f'{ ctx.message.author.mention } укусил(а) { member.mention }', color = color_kus ) )
    await member.send( embed = discord.Embed( description = f'Тебя укусил(а) { ctx.message.author.mention }', color = color_kus ), delete_after = 60 )


@client.command( aliases = [ 'поцеловать', 'цьом', 'чмок' ] )

async def __pocelui( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )

    if member == None or member == ctx.message.author:
        await ctx.send( embed = discord.Embed( description = f'{ member.mention } поцеловал(а) себя', color = color_kus ) )
        return

    await ctx.send( embed = discord.Embed( description = f'{ ctx.message.author.mention } поцеловал(а) { member.mention }', color = color_kus ) )
    await member.send( embed = discord.Embed( description = f'Тебя поцеловал(а) { ctx.message.author.mention }', color = color_kus ), delete_after = 60 )


@client.command( aliases = [ 'ударить', 'втащить', 'ушатать' ] )

async def __udarit( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )

    if member == None or member == ctx.message.author:
        await ctx.send( embed = discord.Embed( description = f'{ member.mention } ударил(а) себя', color = color_kus ) )
        return

    await ctx.send( embed = discord.Embed( description = f'{ ctx.message.author.mention } ударил(а) { member.mention }', color = color_kus ) )
    await member.send( embed = discord.Embed( description = f'Тебя ударил(а) { ctx.message.author.mention }', color = color_kus ), delete_after = 60 )


@client.command( aliases = [ 'облизать', 'лизь', 'лизнуть' ] )

async def __oblizal( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )

    if member == None or member == ctx.message.author:
        await ctx.send( embed = discord.Embed( description = f'{ member.mention } облизал(а) себя', color = color_kus ) )
        return

    await ctx.send( embed = discord.Embed( description = f'{ ctx.message.author.mention } облизал(а) { member.mention }', color = color_kus ) )
    await member.send( embed = discord.Embed( description = f'Тебя облизал(а) { ctx.message.author.mention }', color = color_kus ), delete_after = 60 )



#Экономический бот
@client.event
async def on_member_joim( member ):
    if cursor.execute( f'SELECT id FROM users WHERE id = { member.id }' ).fetchone() is None:
        cursor.execute( f'INSERT INTO users VALUES ("{ member }", { member.id }, 0, 0, 1)' )
        connection.commit()
    else:
        pass


@client.command( aliases = [ 'balance', 'баланс' ] )

async def __balance( ctx, member: discord.Member = None ):
    if member is None:
        await ctx.send( embed = discord.Embed(
            description = f"""Баланс пользователя **{ ctx.author }** составляет **{ cursor.execute( 'SELECT cash FROM users WHERE id = {}'.format( ctx.author.id ) ).fetchone()[0] } :leaves:** """
        ) )
    else:
        await ctx.send( embed = discord.Embed(
            description = f"""Баланс пользователя **{ member }** составляет **{ cursor.execute( 'SELECT cash FROM users WHERE id = {}'.format( member.id ) ).fetchone()[0] } :leaves:** """
        ) )


@client.command( aliases = [ 'award' ] )
@commands.has_permissions( administrator = True )

async def __award( ctx, member: discord.Member = None, amount: int = None ):
    await ctx.channel.purge( limit = 1 )

    if member is None:
        await ctx.send( embed = discord.Embed( description = f'**{ ctx.message.author.mention }**, укажите пользователя, которому желаете добавить определённую сумму!', colour = discord.Color.red() ), delete_after = 5 )

    else:
        if amount is None:
            await ctx.send( embed = discord.Embed( description = f'**{ ctx.message.author.mention }**, укажите сумму, которую желаете добавить на счет пользователя', colour = discord.Color.red() ), delete_after = 5 )

        elif amount < 1:
            await ctx.send( embed = discord.Embed( description = f'**{ ctx.message.author.mention }**, укажите сумму больше 1 :leaves:', colour = discord.Color.red() ), delete_after = 5 )

        else:
            cursor.execute( 'UPDATE users SET cash = cash + {} WHERE id = {}'.format( amount, member.id ) )
            connection.commit()

            await ctx.send( embed = discord.Embed( description = f'На счёт { member.mention } было зачислено { amount } :leaves:', color = color_unban ) )
            await member.send( embed = discord.Embed( description = f'На ваш счёт было зачислено { amount } :leaves:', color = color_unban ) )

@__award.error
async def award_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )


@client.command( aliases = [ 'take' ] )
@commands.has_permissions( administrator = True )

async def __take( ctx, member: discord.Member = None, amount = None ):
    await ctx.channel.purge( limit = 1 )

    if member is None:
        await ctx.send( embed = discord.Embed( description = f'**{ ctx.message.author.mention }**, укажите пользователя, у которого хотите отнять определённую сумму', colour = discord.Color.red() ), delete_after = 5 )

    else:
        if amount is None:
            await ctx.send( embed = discord.Embed( description = f'**{ ctx.message.author.mention }**, укажите сумму, которую хотите отнять у пользователя', colour = discord.Color.red() ), delete_after = 5 )

        elif amount == 'all':
            cursor.execute( 'UPDATE users SET cash = {} WHERE id = {}'.format( 0, member.id ) )
            connection.commit()

        elif int(amount) < 1:
            await ctx.send( embed = discord.Embed( description = f'**{ ctx.message.author.mention }**, укажите сумму больше 1 :leaves:', colour = discord.Color.red() ), delete_after = 5 )

        else:
            cursor.execute( 'UPDATE users SET cash = cash - {} WHERE id = {}'.format( int(amount), member.id ) )
            connection.commit()

            await ctx.send( embed = discord.Embed( description = f'У { member.mention } списали { amount } :leaves:', color = color_ban ) )
            await member.send( embed = discord.Embed( description = f'У вас списали { amount } :leaves:', color = color_ban ) )

@__take.error
async def take_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )


@client.command( aliases = [ 'add-shop', 'add-role' ] )
@commands.has_permissions( administrator = True )

async def __add_shop( ctx, role: discord.Role = None, cost: int = None ):
    await ctx.channel.purge( limit = 1 )

    if role is None:
        await ctx.send( embed = discord.Embed( description = f'**{ ctx.message.author.mention }**, укажите роль, которую вы хотите добавить в магазин', colour = discord.Color.red() ), delete_after = 5 )

    else:
        if cost is None:
            await ctx.send( embed = discord.Embed( description = f'**{ ctx.message.author.mention }**, укажите стоимость для данной роли', colour = discord.Color.red() ), delete_after = 5 )

        elif cost < 1:
            await ctx.send( embed = discord.Embed( description = f'**{ ctx.message.author.mention }**, стоимость роли не может быть такой маленькой', colour = discord.Color.red() ), delete_after = 5 )

        else:
            cursor.execute( 'INSERT INTO shop VALUES ( {}, {}, {} )'.format( role.id, ctx.guild.id, cost ) )
            connection.commit()

            await ctx.send( embed = discord.Embed( description = f'В магазин была добавлена новая роль { role.id }', color = color_main ) )

@__add_shop.error
async def addshop_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )


@client.command( aliases = [ 'remove-shop', 'remove-role' ] )
@commands.has_permissions( administrator = True )

async def __remove_shop( ctx, role: discord.Role = None ):
    await ctx.channel.purge( limit = 1 )

    if role is None:
        await ctx.send( embed = discord.Embed( description = f'**{ ctx.message.author.mention }**, укажите роль, которую вы хотите удалить из магазина', colour = discord.Color.red() ), delete_after = 5 )

    else:
        cursor.execute( 'DELETE FROM shop WHERE role_id = {}'.format( role.id ) )
        connection.commit()

        await ctx.send( embed = discord.Embed( description = f'Роль { role.id } была удалена из магазина!', color = color_ban ) )

@__remove_shop.error
async def removeshop_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )


@client.command( aliases = [ 'shop', 'магазин' ] )

async def __shop( ctx ):
    embed = discord.Embed( title = 'Магазин ролей', color = color_main )

    for row in cursor.execute( 'SELECT role_id, cost FROM shop WHERE id = {}'.format( ctx.guild.id ) ):
        if ctx.guild.get_role( row[0] ) != None:
            embed.add_field(
                name = f'Стоимость { row[1] }',
                value = f'Вы получите роль { ctx.guild.get_role( row[0] ).mention }',
                inline = False
            )

        else:
            pass

    await ctx.send( embed = embed )


@client.command( aliases = [ 'buy', 'купить' ] )

async def __buy( ctx, role: discord.Role = None ):
    await ctx.channel.purge( limit = 1 )

    if role is None:
        await ctx.send( embed = discord.Embed( description = f'**{ ctx.message.author.mention }**, укажите роль, которую вы хотите купить', colour = discord.Color.red() ), delete_after = 5 )

    else:
        if role in ctx.author.roles:
            await ctx.send( embed = discord.Embed( description = f'**{ ctx.message.author.mention}**, у вас уже есть данная роль', colour = discord.Color.red() ), delete_after = 5 )

        elif cursor.execute( 'SELECT cost FROM shop WHERE role_id = {}'.format( role.id ) ).fetchone()[0] > cursor.execute( 'SELECT cash FROM users WHERE id = {}'.format( ctx.author.id ) ).fetchone()[0]:
            await ctx.send( embed = discord.Embed( description = f'**{ ctx.message.author.mentionr }**, у вас недостаточно средств для покупки данной роли', colour = discord.Color.red() ), delete_after = 5 )

        else:
            await ctx.author.add_roles( role )
            cursor.execute( 'UPDATE users SET cash = cash - {0} WHERE id = {1}'.format( cursor.execute( 'SELECT cost FROM shop WHERE role_id = {}'.format( role.id ) ).fetchone()[0], ctx.author.id ) )
            connection.commit()

            await ctx.send( embed = discord.Embed( description = f'{ ctx.message.author.mention }, вы успешно приобрели новую роль', color = color_unban ) )
            #await member.send( embed = discord.Embed( description = 'Вы успешно приобрели новую роль', color = color_unban ) )



#Информация пользователя
@client.command()

async def info( ctx, *, user: discord.User ):
    await ctx.channel.purge( limit = 1 )

    emb = discord.Embed( color = color_main )
    emb.add_field( name = "Имя", value = user.name, inline = False )
    emb.add_field( name = "ID", value = user.id, inline = False )
    #emb.add_field( name = "Присоединился", value = str( user.joined_at )[:16], inline = False )
    emb.add_footer( text = 'Test' )

    await ctx.send( embed = emb )



#Присоединился к нам
@client.event

async def on_member_join( member ):
    channel = client.get_channel( id_connect_server )

    emb = discord.Embed( description = '''
    Приветик!
    Спасибо что заглянул на **Foren Server**.
    Чувствуй себя как дома, только не нарушай правила.
    Держи печеньку 🍪
    ''', color = color_main )

    await member.send( embed = emb )

    await channel.send( embed = discord.Embed( description = f'Пользователь { member.mention }, присоединился к нам!', color = 0xff8000 ) )



#Фильтрация чата
#@client.event

#async def on_message( message ):
    #await client.process_commands( message )

    #msg = message.content.lower()

    #if msg in bad_words:
        #await message.delete()
        #await message.author.send( embed = discord.Embed( description = 'Не надо такое писать! ```Сообщение: {  }```', color = color_warn ), delete_after = 10 )



#Команды не существует
@client.event
async def on_command_error( ctx, error ):
    #await ctx.channel.purge( limit = 1 ) #ОШИБКА С КОМАНДАМИ
    if isinstance( error, commands.CommandNotFound ):
        await ctx.send( embed = discord.Embed( description = f'{ ctx.message.author.mention }, такой команды не существует!', colour = discord.Color.red() ), delete_after = 3 )



#Команда !help
@client.command( aliases = [ 'help', 'помощь', 'хелп' ] )

async def __help( ctx ):
    emb = discord.Embed( title = 'Помощь', color = color_main )

    emb.add_field( name = '{}help-moder'.format( PREFIX ), value = 'Команды для модерации', inline = False )
    emb.add_field( name = '{}help-eco'.format( PREFIX ), value = 'Команды экономического бота', inline = False )
    #emb.add_field( name = '{}help-chat'.format( PREFIX ), value = 'Кикнуть участника', inline = False )

    await ctx.send( embed = emb )


@client.command( aliases = [ 'help-moder' ] )

async def __help_moder( ctx ):
    emb = discord.Embed( title = 'Команды для модерации', color = color_main )

    emb.add_field( name = '{}clear'.format( PREFIX ), value = 'Очистить чат', inline = False )
    emb.add_field( name = '{}ban'.format( PREFIX ), value = 'Забанить участника', inline = False )
    emb.add_field( name = '{}kick'.format( PREFIX ), value = 'Кикнуть участника', inline = False )
    emb.add_field( name = '{}unban'.format( PREFIX ), value = 'Разбанить участника', inline = False )
    emb.add_field( name = '{}mute'.format( PREFIX ), value = 'Заглушить участника', inline = False )
    emb.add_field( name = '{}warn'.format( PREFIX ), value = 'Предупредить участника', inline = False )
    emb.add_field( name = '{}tempban'.format( PREFIX ), value = 'Временно заблокировать участника', inline = False )

    await ctx.send( embed = emb )


@client.command( aliases = [ 'help-eco' ] )

async def __help_eco( ctx ):
    emb = discord.Embed( title = 'Команды экономического бота', color = color_main )

    emb.add_field( name = '{}shop'.format( PREFIX ), value = 'Магазин', inline = False )
    emb.add_field( name = '{}take'.format( PREFIX ), value = 'Забрать деньги', inline = False )
    emb.add_field( name = '{}remove-shop'.format( PREFIX ), value = 'Удалить роль из магазина', inline = False )
    emb.add_field( name = '{}add-shop'.format( PREFIX ), value = 'Добавить роль в магазин', inline = False )
    emb.add_field( name = '{}balance'.format( PREFIX ), value = 'Баланс', inline = False )
    emb.add_field( name = '{}award'.format( PREFIX ), value = 'Дать деньги', inline = False )
    emb.add_field( name = '{}buy'.format( PREFIX ), value = 'Купить роль в магазине', inline = False )

    await ctx.send( embed = emb )



#Подключение
client.run( TOKEN )
