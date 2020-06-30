import discord
from discord.ext import commands
from discord.utils import get

import asyncio

PREFIX = '#'
client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )

@client.event
async def on_command_error( ctx, error ):
    pass

@client.event
async def on_ready():
    print( 'Bot connected v1.0.3' )

    await client.change_presence( status = discord.Status.online, activity = discord.Game( '{}help'.format( PREFIX ) ) )



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



#Очистка сообщений
@client.command()
@commands.has_permissions( administrator = True )

async def clear( ctx, amount = 1 ):
    await ctx.channel.purge( limit = amount+1 )

    await ctx.send( embed = discord.Embed( description = f':white_check_mark: Удалено { amount } сообщений', colour = discord.Color.green() ), delete_after = 1 )

@clear.error
async def clear_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )



#Кик
@client.command()
@commands.has_permissions( administrator = True )

async def kick( ctx, member: discord.Member, *, reason = None ):
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

@kick.error
async def kick_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}kick [@участник] (причина) - кикнуть с сервера```'.format( PREFIX ), delete_after = 5 )



#Бан
@client.command()
@commands.has_permissions( administrator = True )

async def ban( ctx, member: discord.Member, *, reason = None ):
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

@ban.error
async def ban_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}ban [@участник] (причина) - забанить навсегда```'.format( PREFIX ), delete_after = 5 )


#Разбан
@client.command()
@commands.has_permissions( administrator = True )

async def unban( ctx, *, member: discord.Member ):
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

@unban.error
async def unban_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}unban [участник#0000] - разбанить```'.format( PREFIX ), delete_after = 5 )



#Предупреждение
@client.command()
@commands.has_permissions( administrator = True )

async def warn( ctx, member: discord.Member, *, reason ):
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

@warn.error
async def warn_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}warn [@участник] (причина) - предупредить```'.format( PREFIX ), delete_after = 5 )



#Временный бан
@client.command()
@commands.has_permissions( administrator = True )

async def tempban( ctx, member: discord.Member, time: int, *, reason ):
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

@tempban.error
async def tempban_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}tempban [@участник] (время в минутах) (причина) - забанить```'.format( PREFIX ), delete_after = 5 )



#Мут
@client.command()
@commands.has_permissions( administrator = True )

async def mute( ctx, member: discord.Member, time: int, *, reason ):
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

@mute.error
async def mute_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}mute [@участник] (время в минутах) (причина) - заглушить```'.format( PREFIX ), delete_after = 5 )



#Размут
@client.command()
@commands.has_permissions( administrator = True )

async def unmute( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )

    await member.remove_roles( discord.utils.get( ctx.message.guild.roles, id = role_muted ) )

    embed = discord.Embed( description = f'У { member.mention } снят мут', color = color_unban )
    embed.set_footer( text= f"Размучен администратором { ctx.author.name }", icon_url = ctx.author.avatar_url )
    await ctx.send( embed = embed )

    await member.send( embed = discord.Embed( description = f'У вас снято ограничение чата администратором { ctx.author.name }', color = color_unban ) )

@unmute.error
async def unmute_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( embed = insufficient_rights_error, delete_after = 3 )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        await ctx.send( '```{}unmute [@участник] - размутить```'.format( PREFIX ), delete_after = 5 )



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
@client.event

async def on_message( message ):
    await client.process_commands( message )

    msg = message.content.lower()

    if msg in bad_words:
        await message.delete()
        await message.author.send( embed = discord.Embed( description = 'Не надо такое писать! ```Сообщение: {  }```', color = color_warn ), delete_after = 10 )



#Команды не существует
@client.event
async def on_command_error( ctx, error ):
    #await ctx.channel.purge( limit = 1 ) #ОШИБКА С КОМАНДАМИ
    if isinstance( error, commands.CommandNotFound ):
        await ctx.send( embed = discord.Embed( description = f'{ ctx.message.author.mention }, данной команды не существует!', colour = discord.Color.red() ), delete_after = 3 )



#Команда !help
@client.command()

async def help( ctx ):
    emb = discord.Embed( title = 'Команды для модерации', color = color_main )

    emb.add_field( name = '{}clear'.format( PREFIX ), value = 'Очистить чат', inline = False )
    emb.add_field( name = '{}ban'.format( PREFIX ), value = 'Забанить участника', inline = False )
    emb.add_field( name = '{}kick'.format( PREFIX ), value = 'Кикнуть участника', inline = False )
    emb.add_field( name = '{}unban'.format( PREFIX ), value = 'Разбанить участника', inline = False )
    emb.add_field( name = '{}mute'.format( PREFIX ), value = 'Заглушить участника', inline = False )
    emb.add_field( name = '{}warn'.format( PREFIX ), value = 'Предупредить участника', inline = False )
    emb.add_field( name = '{}tempban'.format( PREFIX ), value = 'Временно заблокировать участника', inline = False )
    emb.set_footer( text = 'Версия бота: v1.0.3' )

    await ctx.send( embed = emb )



#Подключение
client.run( TOKEN )
