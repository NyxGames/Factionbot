import discord, os
from datetime import date

# Gets the bot
client = discord.Client()

# Prefix used in the command, e.g: f!displaypoints
prefix = "f!"
debugprefix = "_f!"

playerList = []

setup = False

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(prefix+"date"):
        await client.send_message(message.channel, str(date.today()).split()[0])
    if message.content.startswith(debugprefix+"setup"):
        if message.author.server_permissions.administrator:
            global setup 
            if setup == True: 
                await client.send_message(message.channel, "Bot is already set up")
                return

            await client.send_message(message.channel, "Setting up channels")
            current = discord.utils.get(message.server.channels, name="faction-bot-commands")

            server = message.author.server
            if not current:
                await client.create_channel(server, 'faction-bot-commands', type=discord.ChannelType.text)

            await client.send_message(message.channel, "Setting up roles")
            current = discord.utils.get(message.server.roles, name="bot commander")

            author = message.author
            if not current:
                await client.create_role(author.server, name="bot commander")

            role = discord.utils.get(author.server.roles, name="bot commander")
            await client.add_roles(author, role)

            setup = True

            setupchannel = discord.utils.get(message.server.channels, name="faction-bot-commands")
            await client.send_message(setupchannel, "Hello "+author.name+". You have successfully set up the Facction Bot.")
            await client.send_message(setupchannel, "You have been given the role needed to command me, and you may give anyone else that role.")
            await client.send_message(setupchannel, "If you need help, either use f!help, or contact Nyxie#8439")
            await client.send_message(setupchannel, "I hope this bot is useful :D")
            return
    if not discord.utils.get(message.author.server.roles, name="bot commander"):
        await client.send_message(message.channel, "You don't have permission to use that command")
        return
    if message.content.startswith(prefix+"hello"):
        await client.send_message(message.channel, "Hey there, "+message.author.name)
        return
    if message.content.startswith(prefix+"help"):
        msg = 'f!hello - Says hello to you \nf!help - Displays all commands \nf!givepoints <name> <amount> - Gives points to a user \nf!displaypoints - Shows everyone in the servers points \nf!showpoints <user> - Displays a certain users points'
        em = discord.Embed(title='Basic Commands', description=msg, colour=0x00FF00)
        em.set_author(name='FactionBot', icon_url=client.user.default_avatar_url)
        await client.send_message(message.channel, embed=em)

        msg = 'f!setup - Sets up the bot \n!fdisplaypoints - Displays everyones ID\'s and points'
        em = discord.Embed(title='Debug Commands (Use _f!)', description=msg, colour=0xFF0000)
        em.set_author(name='FactionBot', icon_url=client.user.default_avatar_url)
        await client.send_message(message.channel, embed=em)
    if message.content.startswith(prefix+"givepoints"):
        
        msg = message.content
        tab = msg.split()

        found = False
        for i in playerList:
            if i[0] == tab[1]:
                i[1] += tab[2]
                found = True

        if found == False:
            playerList.append([tab[1], tab[2]])

        setupchannel = discord.utils.get(message.server.channels, name="faction-bot-commands")
        await client.send_message(setupchannel, tab[1]+" has been given <:HivePoint:505423291931164693>"+tab[2]+"!")
        if len(tab) >= 4:
            msg = ''
            x = -1
            for i in tab:
                x += 1
                print(x)
                if x >= 3:
                    msg += i+' '
            
            await client.send_message(setupchannel, "Reason: "+msg)

        return
    
    if message.content.startswith(prefix+"displaypoints"):
        msg = ''
        for i in playerList:
            msg += str(i[0])+": <:HivePoint:505423291931164693>"+str(i[1])+"\n"

        em = discord.Embed(title='', description=msg, colour=0x00FFFF)
        em.set_author(name='FactionBot', icon_url=client.user.default_avatar_url)
        await client.send_message(message.channel, embed=em)
        return

    if message.content.startswith(prefix+"showpoints"):
        msg = message.content
        tab = msg.split()

        for i in playerList:
            if i[0] == tab[1]:
                msg = i[1]
        
        em = discord.Embed(title='', description=tab[1]+' has '+msg+' points!', colour=0x00FFFF)
        em.set_author(name='FactionBot', icon_url=client.user.default_avatar_url)
        await client.send_message(message.channel, embed=em)
        return

    if message.content.startswith(debugprefix+"displaypoints"):
        msg = ''
        for i in playerList:
            msg += str(i[0])+": "+str(i[1])+"\n"

        em = discord.Embed(title=msg, description='', colour=0x00FFFF)
        em.set_author(name='FactionBot', icon_url=client.user.default_avatar_url)
        await client.send_message(message.channel, embed=em)
        return
    

client.run('NTA0OTk1MDAyMjg0MjQ0OTky.DrNJmg.9LCEuksS89YUOdTC-jsN-zXHDrk')