import aiocron
import discord
import locale
import os
import pdf2image
import requests
import time

from datetime import datetime, timedelta
from discord.ext import commands

from weather import get_temperature, get_rain

from dotenv import load_dotenv

load_dotenv(override=True)

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

PRIVATE_CHANNEL_ID = os.environ.get("PRIVATE_CHANNEL_ID")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

bot = commands.Bot(command_prefix="!")

# Obtenir l'heure et la date locale
tomorrow = datetime.today() + timedelta(days=1)
locale.setlocale(locale.LC_TIME, "fr_FR.utf8")

@bot.command(pass_context=True)
async def send(ctx, *, message: str):
    channel = bot.get_channel(int(CHANNEL_ID))
    print(ctx.message.channel.id)
    if ctx.message.channel.id == int(PRIVATE_CHANNEL_ID):
        await channel.send(message)
    else:
        await ctx.message.delete()


@bot.command(pass_context=True)
async def temp(ctx):
    channel = bot.get_channel(int(CHANNEL_ID))
    if ctx.message.channel.id == int(PRIVATE_CHANNEL_ID):
        message_intro = "Bonjour à tous, voici les informations pour demain, {} : ".format(tomorrow.strftime("%A %d %B %Y"))
        temperature = "Température (min - max) : {}".format(get_temperature())
        rain_message = "Il va potentiellement pleuvoir." if get_rain() else "Il ne devrait pas pleuvoir."

        await channel.send("{} \n{} \n{}".format(message_intro, temperature, rain_message))
    else:
        await ctx.message.delete()


@bot.command(pass_context=True)
async def program(ctx):
    channel = bot.get_channel(int(CHANNEL_ID))
    if ctx.message.channel.id == int(PRIVATE_CHANNEL_ID):
        programme = requests.get("https://www.puydufou.com/france/fr/program-day/download-tomorrow")

        screenshot = pdf2image.convert_from_bytes(programme.content)[0]
        screenshot.save("screenshot.png", filename="screenshot.png")

        await channel.send(file=discord.File("screenshot.png"))
    else:
        await ctx.message.delete()


@aiocron.crontab('36 20 * * *')
async def crontestjob(ctx):
    channel = bot.get_channel(int(CHANNEL_ID))
    message_intro = "Bonjour à tous, voici les informations pour demain, le {} : ".format(time.strftime("%A %d %B %Y", now))
    temperature = "Température (min - max) : {}".format(get_temperature())
    rain_message = "Il va potentiellement pleuvoir." if get_rain() else "Il ne devrait pas pleuvoir."

    try:
        programme = requests.get("https://www.puydufou.com/france/fr/program-day/download-tomorrow")

        screenshot = pdf2image.convert_from_bytes(programme.content)[0]
        screenshot.save("screenshot.png", filename="screenshot.png")
        await channel.send("{} \n{} \n{}".format(message_intro, temperature, rain_message), file=discord.File("screenshot.png"))

    except Exception as e:
        await channel.send("{} \n{} \n{} \nMalheureusement, je n'ai pas pu vous récupérer le programme de demain.".format(message_intro, temperature, rain_message))

bot.run(DISCORD_TOKEN)
