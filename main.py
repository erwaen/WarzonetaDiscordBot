# bot.py
import os
import random
import time

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix="!")



lobbyList = []

def verificarTiempo():
    for user in lobbyList:
        
        time_from_started = int(((time.time() - user["enterTime"])/60))
        print("SU TIEMPO ES: " + str(time_from_started))
        if time_from_started >= 15:
            lobbyList.remove(user)

def verificarSiEstaEnLobby(name_user):
    for user in lobbyList:

        if user["name"] == name_user:
            return False
    
    return True



def printLobby():
    response = "Lista de usuarios en lobby:\n"
    for user in lobbyList:
        time_from_started = '%.2f' % ((time.time() - user["enterTime"])/60)
        response += "- " + str(user["name"]) + "\t" + str(time_from_started) + " min\n"
    
    return response


@bot.command(
    name='enter',
    brief="Te pone en la lista del Lobby"
)
async def enterLobby(ctx):
    verificarTiempo()
    response = ""
    if not verificarSiEstaEnLobby(ctx.author.name):
        response = "Ya estas koa vovo!\n\n"
        response += printLobby()
    elif len(lobbyList) < 4:
        newUser = {}
        newUser["name"] = ctx.author.name
        newUser["enterTime"] = time.time()
        print(newUser)
        lobbyList.append(newUser)
        response = "Agregado en la lista!\n\n"
        response += printLobby()
    else: 
        response = "Ya hay 4 en la lista del lobby :(\n" + "a los 15 minutos se elimina a alguien de la lista.\n\n"
        response += printLobby()


    await ctx.send(response)


@bot.command(
    name='lobby',
    brief="Visualizar los usuarios actuales del lobby"
)
async def seeLobby(ctx):
    verificarTiempo()
    response = ""
    if len(lobbyList) == 0:
        response = "Todavia no hay nadie en la lista :("
    else:
        response = printLobby()

    await ctx.send(response)

@bot.command(
    name='removeme',
    brief="Te elimina de la lista del lobby"
)
async def removeme(ctx):
    username = ctx.author.name
    for user in lobbyList:
        if user["name"] == username:
            lobbyList.remove(user)
            await ctx.send(printLobby())
            break
            
    
    
# @bot.command(name='help')
# async def helpCommand(ctx):
#     response ="hola"
#     # response = """ =============COMANDOS===================

#     #     !enter -> Te agrega a la lista para el lobby

#     #     !removeme -> Te quita de la lista

#     #     !lobby -> para visualizar el lobby actual """

#     await ctx.send(response)

bot.run(TOKEN)
