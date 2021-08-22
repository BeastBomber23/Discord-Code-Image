import discord
from discord.ext import commands

from random import randint

import io
import os

import re

from PIL import Image
from urllib.request import urlopen
import urllib.parse

carbonURL = 'https://carbonnowsh.herokuapp.com/?lineNumbers=true&theme=dracula&backgroundColor=rgba(20,20,20,255)&dropShadow=false&code='
discordKey = '' #YOUR DISCORD BOT KEY

client = commands.Bot('.')

def convert(original):
    new = original

    new = new.replace(".code", "")
    new = new.replace(" ", "+")
    new = new.replace('"', "'")
    new = new.replace("&", "|and|")
    new = new.replace("\n", "%250A")

    return new

def saveCode(code, username):

    url = carbonURL + code

    img = Image.open(urlopen(url))
    img_data = img.load()

    height,width = img.size

    for x in range(height):
        for y in range(width):
            r,g,b,a = img_data[x,y]
            if r == 20 & g == 20 & b == 20: #Very similar color to background so we dont get any noticeable artifacts.
                img_data[x,y] = 0,0,0,0

    name = "C:/LOCATION/OF/YOUR/CODE/IMAGE/LOG/FILE/" + "USER" + str(username) + "RANDID" + str(randint(0, 10000)) + ".png" #EDIT THE PATH ON THIS LINE

    print(name)

    img.save(name)

    return name

@client.event
async def on_message(message):
    if message.content.startswith('.code'):
        converted = convert(message.content)

        if "|and|" in converted:
            await message.channel.send("```&(s) have been replaced with |and| by discord bot for api reasons.```")

        name = saveCode(converted, message.author.id)
        await message.channel.send(file=discord.File(name))

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

def setupDiscordBot():
    print("Starting up discord bot")
    client.run(discordKey)

setupDiscordBot()
