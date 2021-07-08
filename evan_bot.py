import json
import random
from bs4 import BeautifulSoup
from discord.ext import commands
from QuestionHelper import QuestionHelper
from Question import Question # !!! is there a better way to import these?

# variables
cp = "!"
test_question = "This is a test"

game = QuestionHelper()
question = Question("","","","","")

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
    msg = msg.lower()
    msg = msg.strip()
    if msg[0] == "!":
        return

    if is_q_active:
        answers[name] = msg
    

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
# !!! dif bwt tf and ma
# !!! check for last question
@client.command()
async def question(ctx):
    global question

    if len(game.question_queue) == 0:
        await ctx.send("The question queue is empty")
        return

    question = game.get_next_question()
    q = BeautifulSoup(question.question, "lxml").get_text()
    
    if question.type == "boolean":
        await ctx.send(q)
    
    else:
        a = BeautifulSoup(get_ans_choices(question), "lxml").get_text()
        msg = q + "\n" + a
        await ctx.send(msg)
    
    global is_q_active
    is_q_active = True

def get_ans_choices(q: Question) -> str:
    ans = q.incorrect_answers
    x = random.randrange(0,len(ans))
    ans.insert(x, q.correct_answer)
    msg = format_list(ans, "or")

    return msg


# ends answering period
@client.command()
async def end(ctx):
    global is_q_active
    is_q_active = False

    ans = question.correct_answer
    correct = list_correct_users(ans)
    correct = strip_username(correct)
    ppl = format_list(correct, "and")
    if ppl == "":
        ppl = "Nobody"
        
    await ctx.send(f"The correct answer was {ans}\n{ppl} got it right!")


def list_correct_users(ans) -> list:
    ans = ans.lower()
    ans = ans.strip()
    correct = []

    for user, answer in answers.items():
        if answer == ans:
            correct.append(user)
    return correct

# !!!sends scores
@client.command()
async def scores():
    return


#helper functions

# turns list into a string with the given conjunction
def format_list(lst: list, conj: str) -> str:
    if len(lst) == 1:
        return str(lst[0])
    else: 
        string = ""
        for i in range(len(lst)):
            if i != (len(lst) - 1):
                string = string + lst[i] + ", "
            else:
                string = string + conj + " " + lst[i]
        return string

# strips numbers from username
def strip_username(users: list) -> list:
    striped_users = [user.split('#')[0] for user in users]
    return striped_users


# run the client on the server
with open("token.json") as json_data:
    data = json.load(json_data)
    token = data["token"]
client.run(token)


