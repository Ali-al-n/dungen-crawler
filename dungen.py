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
        print("You have %s hitpoints" % player1.hitpoints)
# 'elif' is a shorthand for 'else if', for instance if we have more conditions to add
    elif roll > 30:
        damage_taken = math.ceil(random.randrange(10) / 100 * player1.hitpoints)
        player1.hitpoints = player1.hitpoints - damage_taken
        print("\nYou manage to get away, taking %s damage." % damage_taken)
        print("you have %s hitpoints" % player1.hitpoints)
# 'else' is for any condition, if none of the if-statements get hit above, this one will always get hit
    else:
        damage_taken = math.ceil(random.randrange(10) / 100 * player1.hitpoints)
        player1.hitpoints = player1.hitpoints - damage_taken
        print("\nYou fail to run away, taking %s damage." % damage_taken)
        print("you have %s hitpoints" % player1.hitpoints)

def climb():
# roll a random number, 100 is max
    roll = random.randrange(100)
# this is pretty much what it sounds like, if the number rolled is above 50
    if roll > 70:
        print("\nYou sucessfully climbed up!\n")
        print("You have %s hitpoints" % player1.hitpoints)
# 'elif' is a shorthand for 'else if', for instance if we have more conditions to add
    elif roll > 50:
        damage_taken = math.ceil(random.randrange(10) / 100 * player1.hitpoints)
        player1.hitpoints = player1.hitpoints - damage_taken
        if player1.hitpoints <= 0:
            end_game()
        print("\nYou manage to get up, taking %s damage." % damage_taken)
        print("you have %s hitpoints" % player1.hitpoints)
# 'else' is for any condition, if none of the if-statements get hit above, this one will always get hit
    else:
        damage_taken = math.ceil(random.randrange(10) / 100 * player1.hitpoints)
        player1.hitpoints = player1.hitpoints - damage_taken
        print("\nYou fail to climb up, taking %s damage." % damage_taken)
        print("you have %s hitpoints" % player1.hitpoints)
def end_game():
    print("YOU DIED!")
    print("\n Q to quit\n and 1 to play.")
    decision = input("press anything to play\npress Q to quit\n")
    if decision == "Q":
        sys.exit()
    else:
        new_game()
def new_game():
    os.system('clear')
    new_player()
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

def new_player(level=1):
    if 'player1' not in locals() or 'player1' not in globals():
        global player1
        player1 = Player(level)

def play(self):
       if self:
           canvas.canvas()
           x = input("What would you like to do?\n1. Hunt\n2. Scavenge\n3. Rest\n4. Equip item\n5. View Equipment.\n")
           if x == "1":
               self.moveTo(canvas.DWARF)
               self.hunt()
           elif x == "2":
               self.scavenge()
           elif x == "3":
               self.moveTo(canvas.FIRE)
               self.rest()
           elif x == "4":
               canvas.canvas()
               try:
                   x = int(input('Enter slot to equip.\n'))
               except:
                   return
               self.equipItem(x)
           elif x == "5":
               canvas.canvas()
               self.viewEquipment()
           else:
               pass
       else:
           #canvas.canvas()
           x = input("What would you like to do?\n1. Play again\n2. Quit\n")
           if x == "1":
               self.new_player()
               play()

###########################################################################
#                                CLASSES                                  #
###########################################################################

# This is a 'class', or in other words an object which can be anything, and this object has certain things like levels, hitpoints and other things
class Player():
    def __init__(self, level=1):
        self.level = level
        self.maxhitpoints = 15 * 1.05 ** (self.level - 1)
        self.hitpoints = self.maxhitpoints
        self.stamina = 100

###########################################################################
#                                 MAIN                                    #
###########################################################################
os.system('clear')
print("Welcome to our game!\n")

print("made by:\nAli-al-n and \nhaaln\n")

decision = input("press anything to play\npress Q to quit\n")
if decision == "Q":
    sys.exit()

new_game()
