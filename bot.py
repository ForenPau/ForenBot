import discord
from discord.ext import commands
from discord.utils import get

PREFIX = '#'
client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )

@client.event
async def on_command_error( ctx, error ):
    pass

@client.event
async def on_ready():
    print( 'Bot connected v1.0.1' )

    await client.change_presence( status = discord.Status.online, activity = discord.Game( '{}help'.format( PREFIX ) ) )



#Переменные
TOKEN = 'NzI0OTY3NjMxNDcxMzc4NDg0.Xvh6Vg.zOsKJF549-oxks2LdTrgG74y7y4'
ID = 724967631471378484

id_connect_server = 482502913743257600 #Канал для отображения присоединения на сервер

insufficient_rights = 'У вас недостаточно прав на выполнение этой команды!'
insufficient_rights_error = discord.Embed( description = insufficient_rights, colour = discord.Color.red() )
bad_words = [ 'тест' ]



#Очистка сообщений
@client.command()
@commands.has_permissions( administrator = True )

async def clear( ctx, amount = 1 ):
    await ctx.channel.purge( limit = amount+1 )

    await ctx.send( embed = discord.Embed( description = f':white_check_mark: Удалено {amount} сообщений', colour = discord.Color.green() ) )

@clear.error
async def clear_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.send( embed = insufficient_rights_error )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.send( '```{}clear [кол-во] - очистить сообщения```'.format( PREFIX ) )



#Кик
@client.command()
@commands.has_permissions( administrator = True )

async def kick( ctx, member: discord.Member, *, reason = None ):

    if reason == None:
        emb = discord.Embed( description = f'{ ctx.author.name }, обязательно укажи причину!', colour = discord.Color.red() )
        await ctx.send( embed = emb )
        return

    if member == None or member == ctx.message.author:
        emb = discord.Embed( description = f'{ member.mention }, вы не можете кикнуть самого себя', colour = discord.Color.red() )
        await ctx.send( embed = emb )
        return

    await ctx.channel.purge( limit = 1 )

    embb = discord.Embed( description = f'Вы были исключены из **Foren Server** администратором **{ ctx.author.name }** ```Причина: { reason }```', color = 0x0080ff )
    await member.send( embed = embb )

    await member.kick( reason = reason )

    embed = discord.Embed( color = 0x0080ff )
    embed.set_author( name = member.name, icon_url = member.avatar_url )
    embed.add_field( name = "Пользователь", value = format( member.mention ), inline = False )
    embed.add_field( name = "Модератор", value = format( ctx.author.name ), inline = False )
    embed.add_field( name = "Причина", value = reason, inline = False )
    embed.set_footer( text= f"Был исключён администратором { ctx.author.name }", icon_url = ctx.author.avatar_url )

    await ctx.send( embed = embed )

@kick.error
async def kick_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.send( embed = insufficient_rights_error )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.send( '```{}kick [@участник] (причина) - кикнуть с сервера```'.format( PREFIX ) )



#Бан
@client.command()
@commands.has_permissions( administrator = True )

async def ban( ctx, member: discord.Member, *, reason = None ):

    if reason == None:
        emb = discord.Embed( description = f'{ ctx.author.name }, обязательно укажи причину!', colour = discord.Color.red() )
        await ctx.send( embed = emb )
        return

    if member == None or member == ctx.message.author:
        emb = discord.Embed( description = f'{ member.mention }, вы не можете забанить самого себя', colour = discord.Color.red() )
        await ctx.send( embed = emb )
        return

    await ctx.channel.purge( limit = 1 )

    embb = discord.Embed( description = f'Вы были забанены на **Foren Server** администратором **{ ctx.author.name }** ```Причина: { reason }```', color = 0xff0000 )
    await member.send( embed = embb )

    await member.ban( reason = reason )

    embed = discord.Embed( color = 0xff0000 )
    embed.set_author( name = member.name, icon_url = member.avatar_url )
    embed.add_field( name = "Пользователь", value = format( member.mention ), inline = False )
    embed.add_field( name = "Модератор", value = format( ctx.author.name ), inline = False )
    embed.add_field( name = "Причина", value = reason, inline = False )
    embed.add_field( name = "Длительность", value = "∞", inline = False )
    embed.set_footer( text= f"Был забанен администратором { ctx.author.name }", icon_url = ctx.author.avatar_url )

    await ctx.send( embed = embed )

@ban.error
async def ban_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.send( embed = insufficient_rights_error )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.send( '```{}ban [@участник] (причина) - забанить навсегда```'.format( PREFIX ) )


#Разбан
@client.command()
@commands.has_permissions( administrator = True )

async def unban( ctx, *, member ):
    await ctx.channel.purge( limit = 1 )

    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban( user )

        await ctx.send( f'Разбанен { user.mention }' )

        embed = discord.Embed( color = 0x00ff00 )
        embed.set_author( name = member.name, icon_url = member.avatar_url )
        embed.add_field( name = "Пользователь", value = format( member.mention ), inline = False )
        embed.add_field( name = "Модератор", value = format( ctx.author.name ), inline = False )
        embed.set_footer( text= f"Был разбанен администратором { ctx.author.name }", icon_url = ctx.author.avatar_url )

        await ctx.send( embed = embed )

        return

@unban.error
async def unban_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.send( embed = insufficient_rights_error )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.send( '```{}unban [участник#0000] - разбанить```'.format( PREFIX ) )



#Предупреждение
@client.command()
@commands.has_permissions( administrator = True )

async def warn( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )

    if member == None or member == ctx.message.author:
        emb = discord.Embed( description = f'{ member.mention }, вы не можете предупредить самого себя', colour = discord.Color.red() )
        await ctx.send( embed = emb )
        return

    embb = discord.Embed( description = f'Вы были предупреждены на **Foren Server** администратором **{ ctx.author.name }** ```Причина: { reason }```', color = 0xffff00 )
    await member.send( embed = embb )

    embed = discord.Embed( color = 0xffff00 )
    embed.set_author( name = member.name, icon_url = member.avatar_url )
    embed.add_field( name = "Пользователь", value = format( member.mention ), inline = False )
    embed.add_field( name = "Модератор", value = format( ctx.author.name ), inline = False )
    embed.add_field( name = "Причина", value = reason, inline = False )
    embed.set_footer( text= f"Был предупреждён администратором { ctx.author.name }", icon_url = ctx.author.avatar_url )

    await ctx.send( embed = embed )

@warn.error
async def warn_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.send( embed = insufficient_rights_error )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.send( '```{}warn [@участник] (причина) - предупредить```'.format( PREFIX ) )



#Мут
@client.command()
@commands.has_permissions( administrator = True )

async def mute( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )

    if member == None or member == ctx.message.author:
        emb = discord.Embed( description = f'{ member.mention }, вы не можете заглушить самого себя', colour = discord.Color.red() )
        await ctx.send( embed = emb )
        return

    mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Mute' )

    await member.add_roles( mute_role )

    emb = discord.Embed( description = f'У { member.mention } ограничение чата за нарушение прав!', color = 0xff0000 )
    await ctx.send( embed = emb )

    embed = discord.Embed( description = f'У вас ограничение чата на **Foren Server**', color = 0xff0000 )
    await member.send( embed = embed )

@mute.error
async def mute_error( ctx, error ):
    if isinstance( error, commands.MissingPermissions ):
        await ctx.send( embed = insufficient_rights_error )

    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.send( '```{}mute [@участник] (причина) - замутить```'.format( PREFIX ) )



#Присоединился к нам
@client.event

async def on_member_join( member ):
    channel = client.get_channel( id_connect_server )

    emb = discord.Embed( description = '''
    Приветик!
    Спасибо что заглянул на **Foren Server**.
    Чувствуй себя как дома, только не нарушай правила.
    Держи печеньку 🍪
    ''', color = 0xff8000 )

    await member.send( embed = emb )

    await channel.send( embed = discord.Embed( description = f'Пользователь { member.mention }, присоединился к нам!', color = 0xff8000 ) )



#Фильтрация чата
@client.event
async def on_message( message ):
    await client.process_commands( message )

    msg = message.content.lower()

    if msg in bad_words:
        await message.delete()
        await message.author.send( f'{ message.author.name }, не надо такое писать!' )



#Команда !help
@client.command()
#@commands.has_permissions( administrator = True )

async def help( ctx ):
    emb = discord.Embed( title = 'Команды для модерации', color = 0xff8000 )

    emb.add_field( name = '{}clear'.format( PREFIX ), value = 'Очистить чат', inline = False )
    emb.add_field( name = '{}ban'.format( PREFIX ), value = 'Забанить участника', inline = False )
    emb.add_field( name = '{}kick'.format( PREFIX ), value = 'Кикнуть участника', inline = False )
    emb.add_field( name = '{}unban'.format( PREFIX ), value = 'Разбанить участника', inline = False )
    emb.add_field( name = '{}mute'.format( PREFIX ), value = 'Заглушить участника', inline = False )
    emb.add_field( name = '{}warn'.format( PREFIX ), value = 'Предупредить участника', inline = False )

    await ctx.send( embed = emb )



#Подключение
client.run( TOKEN )
