import math
import os
import random
import sys

clear = lambda: os.system('clear')

class Actor():
    def __init__(self, level=1):
        self.level = level
        self.maxhitpoints = 15 * 1.05 ** (self.level - 1)
        self.hitpoints = self.maxhitpoints

    def take_damage(self, damage):
            self.hitpoints = self.hitpoints - damage

    def deal_damage(target):
        damage = random.randrange(1,target.level)
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
            spawn_monster(player)

    def scavenge(self):
        print ("you find the FINAL BOSS")

    def rest(self):
        self.hitpoints = self.maxhitpoints
        print("YOU REST!!! You have %s hitpoints." %self.hitpoints)


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


def run(player):
    roll = random.randrange(100)
    if roll > 50:
        print("\nYou sucessfully run away!\n")
        print("You have %s hitpoints" % player.hitpoints)
        player.is_in_combat = False
    elif roll > 30:
        damage_taken = math.ceil(random.randrange(10) / 100 * player.hitpoints)
        player.hitpoints = player.hitpoints - damage_taken
        print("\nYou manage to get away, taking %s damage." % damage_taken)
        print("you have %s hitpoints" % player.hitpoints)
        player.is_in_combat = False
    else:
        damage_taken = math.ceil(random.randrange(10) / 100 * player.hitpoints)
        player.hitpoints = player.hitpoints - damage_taken
        print("\nYou fail to run away, taking %s damage." % damage_taken)
        print("you have %s hitpoints" % player.hitpoints)

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
    print("You are dumped into a dungeon from high above.\nYou take some damage.\nWhen you land, you faint.\n")
    print("You wake up and see a slime staring at you! You are very scared!\nWhat will you do?")
    player.is_in_combat = True
    while(player.is_in_combat):
        choice = input("\n1. run\n2. climb\n")
        if choice == "1":
            run(player)
        elif choice == "2":
            climb(player)

def hunt():
    roll = random.randrange(100)
    if roll < 15:
        #find_loot
        pass
    else:
        spawn_monster(player)

def spawn_monster(player):
    roll = random.randrange(1000)
    if roll < 5:
        monster = Monster(level = player.level*100, name = "Dragon")
    elif roll < 200:
        monster = Monster(level = player.level+(random.randrange(1, player.level+3)), name = "dark mage")
    elif roll < 700:
        monster = Monster(level = player.level+(random.randrange(1, player.level+1)), name = "slime")
    else:
        monster = Monster(level = player.level+(random.randrange(1, player.level+2)), name = "dwarf")
    fight(player, monster)

def fight(player, monster):
    print("You find a %s, trust me YOU ARE GONNA DIE" %monster.name)
    while player.is_in_combat:
        x = input("1. Attack\n2. Run\n")
        if x == "1":
            attack(player, monster)
        if x == "2":
            run(player)
        else:
            pass
def attack(player, monster):

    dmg = player.deal_damage(monster)
    dmg_mob = monster.deal_damage(player)

    monster.take_damage(dmg)
    print("You strike the %s" %monster.name+" and deal %i damage." %dmg + ' It has %i hitpoints left.' %monster.hitpoints)
    if monster.hitpoints <= 0:
        print('You slay the %s' %monster.name + ' and gain %i EXP' %monster.experience)
        player.addExperience(monster.experience)
        roll = random.randint(1,100)
        if roll > 85:
            #monster_drop = random.choice(monster.dropTable)
            #player.addItem(monster_drop)
            #print('You find a %s.' %monster_drop.name)
            print('You find nothing.')
            pass
        else:
            player.gold += monster.gold
            print('You find %i gold.' %monster.gold)
        del monster
        player.isInCombat = False
    else:
        player.takeDamage(dmg_mob)
    if player.hitpoints <= 0:
        player.isInCombat = False
        new_player()
