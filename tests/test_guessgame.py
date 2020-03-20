import app
from flask import Flask, request, session

app.secret_key = "myStringForEncryption"


### test URLs ###
def test_5000_page(client):
    assert client.get("/").status_code == 404  ## the page is missing


def test_game_page(client):
    response = client.get("/game")
    assert response.status_code == 200  ## the page is responding
    assert response.data.startswith(b"<!DOCTYPE html>") == True  ## the base is used
    assert b'<form method="POST" action="/guessNumber">' in response.data


def test_high_scores(client):
    response = client.get("/highscores")  ## the high score page is loading
    assert response.status_code == 200
    assert response.data.startswith(b"<!DOCTYPE html>") == True  ## the base is used
    assert b"<h2> High Scores </h2>" in response.data


def test_session(client):
    client.get("/game")
    with client.session_transaction() as this_session:
        this_session["randomNumber"] = 3

    response = client.post(
        "/guessNumber", data={"name": "test"}
    )  ## the name of the player
    assert response.status_code == 200
    assert app.start_time() > 0  ## timer started

    response = client.post("/checkNumber", data={"theNumber": "-1"})
    assert "randomNumber" in this_session
    assert this_session["randomNumber"] == 3
    assert request.method == "POST"
    assert response.status_code == 200
    assert (
        b"Sorry the number is too low" in response.data
    )  ## the response considering the number, which is too low

    response = client.post("/checkNumber", data={"theNumber": "1000000"})
    assert "randomNumber" in this_session
    assert this_session["randomNumber"] == 3
    assert request.method == "POST"
    assert response.status_code == 200
    assert (
        b"Sorry the number is too high" in response.data
    )  ## the response considering the number, which is too high

    response = client.post(
        "/checkNumber", data={"theNumber": "3"}
    )  ## the correct number is inserted
    assert "randomNumber" in this_session  ## congratulation page is loaded
    assert response.status_code == 200
    assert b"<h2> Congratulations test ! </h2>" in response.data
    assert session["attempts"] >= 1
