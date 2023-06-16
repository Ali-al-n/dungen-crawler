import sys
import os
import time
print("Welcome to our game!\n")

print("made by:\nali-al-n\nhaaln\n")

# FUNCTIONS 
clear = lambda: os.system('clear')

decision = input("press anything to play\npress Q to quit\n")
if decision == "Q":
    sys.exit()

clear()
print("You are dumped into a dungeon from high above.\nYou take some damage.\nWhen you land, you faint.\n")
time.sleep(3)
print("You wake up and see a slime staring at YOU! You are very scared!\nWhat will you do?")
time.sleep(2)
choice = input("\n1. run\n2. climb\n")
