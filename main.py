from dotenv import load_dotenv
import os
import discord
from datetime import datetime
import logging
import sys


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

load_dotenv()
logChannelId = (os.getenv('logChannel'))
voiceMaster = int((os.getenv('voiceMaster')))
owoner = int((os.getenv('owoner')))


@client.event
async def on_ready():
    await client.wait_until_ready()
    await client.change_presence(activity=discord.Game(name="debug"))
    logger.info('Client is Started')
    print('Client is Ready!')


@client.event
async def on_message_delete(message):
    logger.info(f"{message.author} Deleted: '{message.content}'")
    logChannel = client.get_channel(int(logChannelId))
    embed = discord.Embed(
        title=f"{message.author}'s Message was Deleted",
        description=f"Deleted message: '{message.content}'\nAuthor: {message.author.mention}\n Location: {message.channel.mention}",
        timestamp=datetime.now(),
        color=discord.Colour.red()
    )
    embed.set_footer(text='raicanLog-1.3')
    await logChannel.send(embed=embed)


@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None:  # Log if a Member joinned to a Voice Channel.
        if after.channel.id == voiceMaster:
            return
        elif after.channel.id:
            logger.info(f'{member.name} Joinned {after.channel.name}')
            logChannel = client.get_channel(int(logChannelId))
            embed = discord.Embed(
                title=f"{member.name} Joined a Channel",
                description=f"Channel: <#{after.channel.id}>",
                timestamp=datetime.now(),
                color=discord.Colour.green()
            )
            embed.set_footer(text='raicanLog-1.3')
            await logChannel.send(embed=embed)
    if after.channel is None:  # Log if a Member Left a Voice Channel
        if before.channel.id == voiceMaster:
            return
        else:
            logger.info(f'{member.name} Left {before.channel.name}')
            logChannel = client.get_channel(int(logChannelId))
            embed = discord.Embed(
                title=f"{member.name} Left a Voice Channel",
                description=f"Channel: <#{before.channel.id}>",
                timestamp=datetime.now(),
                color=discord.Colour.orange()
            )
            embed.set_footer(text='raicanLog-1.3')
            await logChannel.send(embed=embed)

    if before.channel and after.channel and after.channel.id != voiceMaster:  # Log if a Member Switch to another Voice Channel.
        if before.channel.id == voiceMaster:  # Log if a Member Created a Voice Channel using VoiceMaster.
            logger.info(f'{member.name} Created {after.channel.name}')
            logChannel = client.get_channel(int(logChannelId))
            embed = discord.Embed(
                title=f"{member.name} Created a Channel",
                description=f"Channel: <#{after.channel.id}>",
                timestamp=datetime.now(),
                color=discord.Colour.green()
            )
            embed.set_footer(text='raicanLog-1.3')
            await logChannel.send(embed=embed)

        elif before.channel and after.channel and after.channel != before.channel:
            logger.info(
                f'{member.name} Switch from {before.channel.name} to {after.channel.name}')
            logChannel = client.get_channel(int(logChannelId))
            embed = discord.Embed(
                title=f"{member.name} Switched Voice Channel",
                description=f"Channel: <#{after.channel.id}>",
                timestamp=datetime.now(),
                color=discord.Colour.green()
            )
            embed.set_footer(text='raicanLog-1.3')
            await logChannel.send(embed=embed)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.id == owoner and message.content.startswith('!rLog --version'):
        await message.channel.send('raicanLog-1.3')
    if message.author.id != owoner and message.content.startswith('!rLog --version'):
        logger.info(f'{message.author.name} tried to use !rLog')
        await message.channel.send(f'{message.author.mention}**No Permission**')

client.run(os.getenv('TOKEN'))
