# evan_bot
Trivia game bot for Discord

Evanbot utilizes the Discord API and Open Trivia Database API https://opentdb.com,
to create a trivia game that can be played on a Discord server. Players have access
to over 4,000 questions from 25 different categories. Evanbot tracks user answers and
awards points for correct answers. Player scores are stored and can be display on 
resquest or at the end of the game. 


## Bot Commands
!setup numOfQuestions categoryNumber
- prepares a game with the given number of questions in the given category

!question
- sends the next question to the chat

!ans
- ends the answering period for the question and updates player scores

!categories
- list all of the category options and their corresponding numbers

!score
- displays the player scores

!end
- ends the game and displays the final scores
