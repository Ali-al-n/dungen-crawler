#!/usr/bin/python3

import sys
import os

import actor

os.system('clear')
print("Welcome to our game!")

print("made by:\nAli-al-n and \nhaaln\n")

decision = input("press anything to play\npress Q to quit\n")
if decision == "Q":
    os.system.exit()


actor.new_game()

while True:
    actor.play(actor.player)
