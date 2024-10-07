import math
import random
import math

import actor
import canvas
import log
import items

def attack(player, monster):

    dmg = player.dealDamage(monster)
    dmg_mob = monster.dealDamage(player)

    log.history.append("The %s" %monster.name +  " deals %i damage." %dmg_mob)
    monster.takeDamage(dmg)
    log.history.append("You strike the %s" %monster.name+" and deal %i damage." %dmg + ' It has %i hitpoints left.' %monster.hitpoints)
    if monster.hitpoints <= 0:
        log.history.append('You slay the %s' %monster.name + ' and gain %i EXP' %monster.experience)
        player.addExperience(monster.experience)
        roll = random.randint(1,100)
        if roll > 85:
            monster_drop = random.choice(monster.dropTable)
            player.addItem(monster_drop)
            log.history.append('You find a %s.' %monster_drop.name)
        else:
            player.gold += monster.gold
            log.history.append('You find %i gold.' %monster.gold)
        del monster
        player.moveTo(canvas.TREASURE_CHEST)
        player.isInCombat = False
    else:
        player.takeDamage(dmg_mob)
    if player.hitpoints <= 0:
        player.isInCombat = False
        player.moveTo(canvas.DEATH)
        actor.new_player()

def run(player, monster):
    roll = random.randrange(100)
    if roll > 75:
        player.moveTo(canvas.EMPTY_PIC)
        log.history.append("You sucessfully run away!")
        player.isInCombat = False
    elif roll > 30:
        player.location = player.moveTo(canvas.EMPTY_PIC)
        damage_taken = monster.dealDamage(player)
        player.takeDamage(damage_taken)
        if player.hitpoints <= 0:
            player.isInCombat = False
            player.moveTo(canvas.DEATH)
            actor.new_player()
        player.isInCombat = False
        log.history.append("You manage to get away, taking %s damage." % damage_taken)
    else:
        damage_taken = monster.dealDamage(player)
        player.takeDamage(damage_taken)
        log.history.append("You fail to run away, taking %s damage." % damage_taken)
        if (player.hitpoints) <= 0:
            player.isInCombat = False
            player.moveTo(canvas.DEATH)
            actor.new_player()

def combat(player, monster):
    while player.isInCombat:
        canvas.canvas()
        x = input("What would you like to do?\n1. Attack\n2. Items\n3. Run\n")
        if x == "1":
            attack(player, monster)
        elif x == "2":
            player.useItem()
        elif x == "3":
            run(player, monster)
        else:
            pass

def combat_encounter(player):
    if player.counter == 5:
        monster = actor.Monster(name='dragon', level=random.randint(player.level,player.level+6))
        player.moveTo(canvas.DWARF)
    roll = random.randint(0,100)
    if roll >= 90:
        monster = actor.Monster(name='Devil Dwarf', level=random.randint(player.level,player.level+2))
        player.moveTo(canvas.DWARF)
    elif roll >= 10:
        monster = actor.Monster(name='Dwarf', level=random.randint(player.level,player.level+1))
        player.moveTo(canvas.DWARF)
    else:
        monster = actor.Monster(name='Drunken Dwarf', level=player.level)
        monster.takeDamage(monster.hitpoints*0.3)
        player.moveTo(canvas.DRUNKEN_DWARF)

    # make monster range go from player level -2 to +2

    player.isInCombat = True
    log.history.append("You encounter a level %i" %monster.level+" %s!" %monster.name)
    combat(player, monster)

def random_encounter(self):
    roll = random.randint(0,100)
    if roll > 90:
        self.moveTo(canvas.EMPTY_PIC)
        log.history.append("You find a boon. Your max HP is increased by 10 %.")
        canvas.canvas()
        self.maxHP = math.ceil(self.maxHP*1.1)
        self.healHP(self.maxHP)
        return
    elif roll > 70:
        self.moveTo(canvas.TREASURE_CHEST)
        item = random.choice(items.item_pool)
        log.history.append('You found a treasure chest with a %s.' % item.name)
        self.addItem(item)
        canvas.canvas()
    else:
        combat_encounter(self)