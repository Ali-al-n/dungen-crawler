#!/usr/bin/python3

import sys
import os

import actor

os.system('clear')
print("Welcome to our game!")

print("made by:\nAli-al-n and \nhaaln\n")

decision = input("press anything to play\npress Q to quit\n")
if decision == "Q" or decision == "q":
    print("Good bye!!!")
    import time
    time.sleep(3)
    print("hold on one sec")
    time.sleep(2)
    print("ther we go")
    time.sleep(0.5)
    os.system('clear')
    sys.exit()


actor.new_game()

while True:
    actor.play(actor.player)
