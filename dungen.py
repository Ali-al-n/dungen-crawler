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
print("You were dumped into a dungeon from high above.\nYou took some damage.\nWhen you landed, you fainted.\n")
time.sleep(2)
print("You wake up and see a slime staring at YOU! You are very scared!\nWhat will you do?")
time.sleep(1)
choice = input("\n1. run\n2. climb")
    


