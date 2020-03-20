import time
import random

number = random.randint(1, 1001)
count = 0
numberInput = 0
startTime = time.time()


def guessNumber(number):
    """ This method will start a timer, and then challange the user to guess a number.
        When the user will guess that secret number, the timer will be stopped and the 
        user's timming will be saved in a file. """

    while numberInput != number:
        numberInput = int(input("Enter another number: "))
        count += 1
        if numberInput < number:
            print("Sorry, your number is too low!")
        elif numberInput > number:
            print("Sorry, your number is too high!")

    endTime = time.time()
    totalTime = endTime - startTime
    seconds = int(totalTime % 60)
    totalTime = totalTime / 60
    minutes = int(totalTime)

    name = input("Enter your name: ")
    print(
        f"Congratulations {name}, you guessed correctly!! The number was {number} and you guessed it after {count} tryes. \nYou guessed in {minutes} minutes and {seconds} seconds\n"
    )

    records = open("records.txt", "a+")
    records.write(
        f"\n{name} had guessed after {number} tries in {minutes} minutes and {seconds} seconds."
    )
    records.close()
