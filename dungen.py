###########################################################################
#                               IMPORTS                                   #
###########################################################################
import sys
import os
import time
import random
import math
###########################################################################
#                               FUNCTIONS                                 #
###########################################################################

# FUNCTIONS 
clear = lambda: os.system('clear')

# This is a how to write a function
def run():
# roll a random number, 100 is max
    roll = random.randrange(100)
# this is pretty much what it sounds like, if the number rolled is above 50
    if roll > 50:
        print("\nYou sucessfully run away!\n")
        print("You have %s hitpoints" % Player.hitpoints)
# 'elif' is a shorthand for 'else if', for instance if we have more conditions to add
    elif roll > 30:
        damage_taken = math.ceil(random.randrange(10) / 100 * Player.hitpoints)
        Player.hitpoints = Player.hitpoints - damage_taken
        print("\nYou manage to get away, taking %s damage." % damage_taken)
        print("you have %s hitpoints" % Player.hitpoints)
# 'else' is for any condition, if none of the if-statements get hit above, this one will always get hit
    else:
        damage_taken = math.ceil(random.randrange(10) / 100 * Player.hitpoints)
        Player.hitpoints = Player.hitpoints - damage_taken
        print("\nYou fail to run away, taking %s damage." % damage_taken)
        print("you have %s hitpoints" % Player.hitpoints)

def climb():
# roll a random number, 100 is max
    roll = random.randrange(100)
# this is pretty much what it sounds like, if the number rolled is above 50
    if roll > 70:
        print("\nYou sucessfully climbed up!\n")
        print("You have %s hitpoints" % Player.hitpoints)
# 'elif' is a shorthand for 'else if', for instance if we have more conditions to add
    elif roll > 50:
        damage_taken = math.ceil(random.randrange(10) / 100 * Player.hitpoints)
        Player.hitpoints = Player.hitpoints - damage_taken
        if Player.hitpoints <= 0:
            print("YOU DIED!")
            end_game()
        print("\nYou manage to get up, taking %s damage." % damage_taken)
        print("you have %s hitpoints" % Player.hitpoints)
# 'else' is for any condition, if none of the if-statements get hit above, this one will always get hit
    else:
        damage_taken = math.ceil(random.randrange(10) / 100 * Player.hitpoints)
        Player.hitpoints = Player.hitpoints - damage_taken
        print("\nYou fail to climb up, taking %s damage." % damage_taken)
        print("you have %s hitpoints" % Player.hitpoints)

###########################################################################
#                                CLASSES                                  #
###########################################################################

# This is a 'class', or in other words an object which can be anything, and this object has certain things like levels, hitpoints and other things
class Player:
    level = 1
    hitpoints = 15
    stamina = 100

###########################################################################
#                                 MAIN                                    #
###########################################################################
print("Welcome to our game!\n")

print("made by:\nAli-al-n and \nhaaln\n")

decision = input("press anything to play\npress Q to quit\n")
if decision == "Q":
    sys.exit()

clear()
print("You are dumped into a dungeon from high above.\nYou take some damage.\nWhen you land, you faint.\n")
#time.sleep(3)
print("You wake up and see a slime staring at you! You are very scared!\nWhat will you do?")
#time.sleep(2)
choice = input("\n1. run\n2. climb\n")
if choice == "1":
    run()
elif choice == "2":
    climb()