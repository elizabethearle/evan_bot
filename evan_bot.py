import requests
import json
from discord.ext import commands

# variables
cp = "!"
test_question = "This is a test"

answers = dict()
is_q_active = False


# set up bot
client = commands.Bot(command_prefix= cp)

client.command_prefix = cp


# records responses
@client.event
async def on_message(message):
    await client.process_commands(message)

    name = str(message.author)
    msg = str(message.content)

    if is_q_active:
        answers[name] = msg.lower()
    

# sends a question to the chat
@client.command()
async def question(ctx):
    await ctx.send(test_question)
    global is_q_active
    is_q_active = True


# ends answering period
@client.command()
async def end(ctx):
    global is_q_active
    is_q_active = False
    print(answers)

@client.command()
async def next(ctx):
    await question(ctx)


# runs the client on the server
with open("token.json") as json_data:
    data = json.load(json_data)
    token = data["token"]
client.run(token)