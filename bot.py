import os
import aiocron
import discord

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

# ID du channel général
CHANNEL_ID = 573125866952065025

def get_channel(channels, channel_name):
    for channel in client.get_all_channels():
        print(channel)
        if channel.name == channel_name:
            return channel
    return None


@client.event
async def on_ready():
    print('Logged on as', client.user)

@client.event
async def on_message(message):
    if message.author == client.user:
       return

    if message.content == 'ping':
       await message.channel.send('pong')

    if message.content == 'temp':
       await message.channel.send(file=discord.File('temperature.png'))

    if message.content == 'humidité':
        await message.channel.send(file=discord.File('humidity.png'))

# MESSAGE AUTOMATIQUE
#@aiocron.crontab('24 * * * *')
#async def crontestjob():
#    channel = client.get_channel(CHANNEL_ID)
#    await channel.send('test message automatique')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, bienvenue sur mon serv'
    )

client.run(DISCORD_TOKEN)
