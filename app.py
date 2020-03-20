# Theodora Tataru
# C00231174
# Guessing Game

from flask import Flask, render_template, request, session
import time
import random
import pickle
import os

app = Flask(__name__)

app.secret_key = "myStringForEncryption"


def rank_player(highscores, player):
    """ Getting the rank of the player from the the sorted pickle file and rewrite the rank numbers """
    with open("highscores.pickle", "rb") as open_file:
        old_list = pickle.load(open_file)
    count = 1
    for item in old_list:
        item[2] = count
        count += 1
    with open("highscores.pickle", "wb") as open_file:
        pickle.dump(old_list, open_file)
    rank = [count for count, element in enumerate(highscores) if element[0] == player]
    ## we get back a list, so we return the element from it, adding one, as it starts from 0
    return int(rank[0]) + 1


def sort_pickle_file(highscores):
    """ Sort the pickle file by attempts and then by time """
    return sorted(highscores, key=lambda player: (player[6], player[4]))


def start_time():
    """ The moment the user starts the game """
    return time.time()


def end_time():
    """ The moment the user guessed the number, and the timer stops"""
    return time.time()


def pick_random_number():
    return random.randint(1, 1000)


def total_time(start, end):
    totalTime = end - start
    return totalTime


####################################################################################################
## homepage!
@app.route("/game")
def welcome_page():
    session["randomNumber"] = pick_random_number()  ##generate random number
    return render_template(
        "index.html", the_title="Welcome to 'Guess The number' Game!"
    )


## geting the name of the player, start timmer, intialize the attempts, generate random number
@app.route("/guessNumber", methods=["POST"])
def start_game():
    session["startTime"] = start_time()  ##start timer
    session["attempts"] = 1  ##initialize number of attempts
    session["player"] = request.form["name"]  ##get player name
    ## print in terminal, for the programmer
    print("::::::::::::::::: The Random Number Is: ", session["randomNumber"])
    print("::::::::::::::::: The Player Name Is: ", session["player"])
    return render_template(
        "guessNumber.html",
        the_title="Enter your number!",
        randomNumber=session["randomNumber"],
    )


## check the player guesses
@app.route("/checkNumber", methods=["POST"])
def check_number():
    formNumber = int(request.form["theNumber"])
    randomNumber = int(session["randomNumber"])
    if randomNumber > formNumber:
        session["attempts"] += 1
        return render_template(
            "guessNumber.html",
            lessOrGrater="Sorry the number is too low",
            the_title="Enter your numbers!",
            randomNumber=session["randomNumber"],
        )
    elif randomNumber < formNumber:
        session["attempts"] += 1
        return render_template(
            "guessNumber.html",
            lessOrGrater="Sorry the number is too high",
            the_title="Enter your numbers!",
            randomNumber=session["randomNumber"],
        )
    else:
        session["endTime"] = end_time()
        session["totalTime"] = total_time(session["startTime"], session["endTime"])

        exists = os.path.isfile("highscores.pickle")  ## check if the file exists
        ## adding current player's details to a new dictionary
        ## I think python gets confused with the [] from session with the [] ones from the list so:
        player = session["player"]
        time = session["totalTime"]
        attempts = session["attempts"]
        rank = 1
        currentPlayer = [player, "Rank", rank, "Total Time", time, "Attempts", attempts]
        ######################################################################################
        if exists:
            ## open pickle file
            with open("highscores.pickle", "rb") as open_file:
                old_list = pickle.load(open_file)
            old_list.append(currentPlayer)  ## update the dictionary, from the file
            ## sort the file
            sortedHighScores = sort_pickle_file(old_list)
            ## rewrite the pickle file with the updatae
            with open("highscores.pickle", "wb") as open_file:
                pickle.dump(sortedHighScores, open_file)

            ## get the rank of the player
            rank = rank_player(sortedHighScores, player)
        else:
            record_score = []
            record_score.append(currentPlayer)
            with open("highscores.pickle", "wb") as open_file:
                pickle.dump(record_score, open_file)
            ## being first, the player gets the 1th rank
            rank = 1
        # print(high_score)
        return render_template(
            "congratulations.html",
            totalTime=session["totalTime"],
            the_title="Well Done!!",
            trying=session["attempts"],
            name=session["player"],
            rank=rank,
        )


@app.route("/highscores")
def high_scores():
    with open("highscores.pickle", "rb") as open_file:
        old_list = pickle.load(open_file)
    sortedHighScores = sort_pickle_file(old_list)
    return render_template(
        "scores.html", the_title="High Scores", data=sortedHighScores
    )


if __name__ == "__main__":
    app.run(debug=True)
