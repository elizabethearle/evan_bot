import requests
import json
from discord.ext import commands

cp = '!'

client = commands.Bot(command_prefix= cp)

client.command_prefix = cp # Setting the prefix of the bot to reflect everywhere it is mentioed


@client.event
async def on_message(message):
    await client.process_commands(message)

    text = str(message.content)

    if not (message.author == client.user) and not(client.command_prefix == text[0]):
        await message.channel.send("wow a message!")
    


@client.command()
async def hi(ctx):
    await ctx.send("hello")


# run the client on the server
client.run('ODU1MjA4OTAzNDY0NTgzMTY4.YMvJWw.Fs19c3W1QAPAd5jfXCTfCw8QPZw')