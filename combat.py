import actor
import random
import math

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

def spawn_monster(player):
    roll = random.randrange(1000)
    if roll < 5:
        monster = actor.Monster(level = player.level*100, name = "Dragon")
    elif roll < 200:
        monster = actor.Monster(level = player.level+(random.randrange(1, player.level+3)), name = "dark mage")
    elif roll < 700:
        monster = actor.Monster(level = player.level+(random.randrange(1, player.level+1)), name = "slime")
    else:
        monster = actor.Monster(level = player.level+(random.randrange(1, player.level+2)), name = "dwarf")
    player.is_in_combat = True
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
