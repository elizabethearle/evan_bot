import requests
import json
from discord.ext import commands
from QuestionHelper import QuestionHelper
from Question import Question # !!! is there a better way to import these?

# variables
cp = "!"
test_question = "This is a test"

game = QuestionHelper()

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
    
# sets up category and stuff
@client.command()
async def setup(ctx, num_questions, category):
    if not(game.is_category(category)):
        return
    num_questions = int(num_questions)
    category_name = ""
    game.set_category(category)
    game.get_session_token()
    actual_num = game.load_questions(num_questions)

    for c in game.list_categories():
        if c["id"] == int(category):
            category_name = c["name"]

    await ctx.send(f"A game with {actual_num} questions in the category {category_name} is ready")
    await ctx.send("Use !question to get the next question")


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

# sends scores
@client.command()
async def scores():
    return


# run the client on the server
with open("token.json") as json_data:
    data = json.load(json_data)
    token = data["token"]
client.run(token)