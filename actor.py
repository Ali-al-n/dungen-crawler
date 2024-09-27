import math
import os
import random
import sys

import combat

clear = lambda: os.system('clear')

class Actor():
    def __init__(self, level=1):
        self.level = level
        self.maxhitpoints = 15 * 1.05 ** (self.level - 1)
        self.hitpoints = self.maxhitpoints

    def take_damage(self, damage):
            self.hitpoints -= damage

    def deal_damage(target):
        damage = random.randrange(target.level)
        return damage

class Player(Actor):
    def __init__(self, level=1):
        self.level = level
        self.stamina = 100
        self.maxhitpoints = 15 * 1.05 ** (self.level - 1)
        self.hitpoints = self.maxhitpoints
        self.gold = 0
        self.experience = 0
        self.is_in_combat = False

    def hunt(self):
        roll = random.randrange(100)
        if roll < 15:
            #find_loot
            pass
        else:
            combat.spawn_monster(player)

    def scavenge(self):
        print ("you find the FINAL BOSS")

    def rest(player):
        player.hitpoints = player.maxhitpoints
        print("YOU REST!!! You have %i hitpoints." %player.hitpoints)

    def addExperience(self, exp):
        self.experience += exp

class Monster(Actor):
    def __init__(self, level=1, name='FINAL BOSS'):
        self.level = level
        self.gold = self.level + random.randrange(20)
        self.name = name
        self.experience = self.level*4
        self.maxhitpoints = 15 * 1.05 ** (self.level - 1)
        self.hitpoints = self.maxhitpoints

def new_player(level=1):
    if 'player1' not in locals() or 'player1' not in globals():
        global player
        player = Player(level)

def play(self):
       #clear()
       if self:
           x = input("What would you like to do?\n1. Hunt\n2. Scavenge\n3. Rest\n")
           if x == "1":
               self.hunt()
           elif x == "2":
               self.scavenge()
           elif x == "3":
               self.rest()
       else:
           x = input("What would you like to do?\n1. Play again\n2. Quit\n")
           if x == "1":
               self.new_player()
               play()

def climb(player):
    roll = random.randrange(100)
    if roll > 70:
        print("\nYou sucessfully climbed up!\n")
        print("You have %s hitpoints" % player.hitpoints)
        player.is_in_combat = False
    elif roll > 50:
        damage_taken = math.ceil(random.randrange(10) / 100 * player.hitpoints)
        player.hitpoints = player.hitpoints - damage_taken
        if player.hitpoints <= 0:
            end_game()
        print("\nYou manage to get up, taking %s damage." % damage_taken)
        print("you have %s hitpoints" % player.hitpoints)
        player.is_in_combat = False
    else:
        damage_taken = math.ceil(random.randrange(10) / 100 * player.hitpoints)
        player.hitpoints = player.hitpoints - damage_taken
        print("\nYou fail to climb up, taking %s damage." % damage_taken)
        print("you have %s hitpoints" % player.hitpoints)

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
    print("You are dumped into a dungeon from high above.\n")
    damage = random.randrange(1,3)
    player.take_damage(damage)
    print('You take %s damage from the fall.' %  damage + 'You have %i Hitpoints' %player.hitpoints)
    print("You are very scared!\nWhat will you do?")
    choice = input("\n1. Find a safe place\n2. Rest and heal.\n")
    if choice == "1":
        player.hitpoints = player.maxhitpoints
        print('You find a safe place.\n')
        play(player)
    elif choice == "2":
        player.rest()

def hunt():
    roll = random.randrange(100)
    if roll < 15:
        #find_loot
        print('you find loot')
        print('!!!currently not working!!!')
        pass
    else:
        combat.spawn_monster(player)
