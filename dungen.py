import sys
import os

import actor

###########################################################################
#                                 MAIN                                    #
###########################################################################
os.system('clear')
print("Welcome to our game!\n")

print("made by:\nAli-al-n and \nhaaln\n")

decision = input("press anything to play\npress Q to quit\n")
if decision == "Q":
    sys.exit()


actor.new_game()

while True:
    actor.play(actor.player)
