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
scores = dict()
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
        if not(name in scores):
            scores[name] = 0
    

# sets up category and stuff
@client.command()
async def setup(ctx, num_questions, category):
    if not(game.is_category(category)):
        await ctx.send("The number you entered doesn't seem to correspond to a category. Here are the categories:\n" + categories())
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
    global question

    if len(game.question_queue) == 0:
        await ctx.send("The question queue is empty")
        return

    question = game.get_next_question()
    q = BeautifulSoup(question.question, "lxml").get_text()
    
    if question.type == "boolean":
        await ctx.send("True or False: " + q)
    
    else:
        a = BeautifulSoup(get_ans_choices(question), "lxml").get_text()
        msg = q + "\n" + a
        await ctx.send(msg)
    
    global is_q_active
    is_q_active = True


# ends answering period
@client.command()
async def end(ctx):
    global is_q_active
    global scores
    is_q_active = False

    ans = question.correct_answer
    correct = list_correct_users(ans)

    for name in correct:
        scores[name] = scores[name] + 1

    correct = strip_username(correct)
    ppl = format_list(correct, "and")
    if ppl == "":
        ppl = "Nobody"
        
    await ctx.send(f"The correct answer was {ans}\n{ppl} got it right!")


# sends category list
@client.command()
async def categories(ctx):
    await ctx.send(categories())


# sends scores
@client.command()
async def score(ctx):
    if scores == {}:
        await ctx.send("There currently are no scores")
    else:
        await ctx.send(format_scores(scores))


# ends the game
# !!! what are you doing with token?
@client.command()
async def end_game(ctx):
    await ctx.send(f"The final scores are:\n {format_scores(scores)}")



# helper functions

#formats scores
def format_scores(scores) -> str:
    players = scores.keys()
    score_str = ""
    for p in players:
        score_str = score_str + strip_single_username(p) + ": " + str(scores[p]) + "\n"
    return score_str


#returns categories as a string
def categories():
    category_list = ""
    for cat in game.list_categories():
        category_list = category_list + str(cat["id"]) + ". " + str(cat["name"]) + "\n"
    return category_list


# makes a string with the answer options to the question
def get_ans_choices(q: Question) -> str:
    ans = q.incorrect_answers
    x = random.randrange(0,len(ans))
    ans.insert(x, q.correct_answer)
    msg = format_list(ans, "or")

    return msg

# lists the users who got the given answer
def list_correct_users(ans) -> list:
    ans = ans.lower()
    ans = ans.strip()
    correct = []

    for user, answer in answers.items():
        if answer == ans:
            correct.append(user)
    return correct

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

# strips numbers from usernames
def strip_username(users: list) -> list:
    striped_users = [user.split('#')[0] for user in users]
    return striped_users

# strips number from a username
def strip_single_username(user):
    user = user.split('#')[0]
    return user


# run the client on the server
with open("token.json") as json_data:
    data = json.load(json_data)
    token = data["token"]
client.run(token)


