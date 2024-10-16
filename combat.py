import math
import random
import math

import render
import actor
import items


def attack(player, monster):
    dmg = player.dealDamage(monster)
    dmg_mob = monster.dealDamage(player)

    render.HISTORY.append("The %s" % monster.name + " deals %i damage." % dmg_mob)
    monster.takeDamage(dmg)
    render.HISTORY.append(
        "You strike the %s" % monster.name
        + " and deal %i damage." % dmg
        + " It has %i hitpoints left." % monster.hitpoints
    )
    if monster.hitpoints <= 0:
        render.HISTORY.append(
            "You slay the %s" % monster.name + " and gain %i EXP" % monster.experience
        )
        player.addExperience(monster.experience)
        roll = random.randint(1, 100)
        if roll > 85:
            monster_drop = random.choice(monster.dropTable)
            player.addItem(monster_drop)
            render.HISTORY.append("You find a %s." % monster_drop.name)
        else:
            player.gold += monster.gold
            render.HISTORY.append("You find %i gold." % monster.gold)
        del monster
        player.location = render.TREASURE_CHEST
        player.isInCombat = False
    else:
        player.takeDamage(dmg_mob)
    if player.hitpoints <= 0:
        player.isInCombat = False
        player.location = render.DEATH
        PLAY = 0
        return PLAY
        # actor.new_player()


def run(player, monster):
    roll = random.randrange(100)
    if roll > 75:
        player.location = render.EMPTY_PIC
        render.HISTORY.append("You sucessfully run away!")
        player.isInCombat = False
    elif roll > 30:
        player.location = player.location = render.EMPTY_PIC
        damage_taken = monster.dealDamage(player)
        player.takeDamage(damage_taken)
        if player.hitpoints <= 0:
            player.isInCombat = False
            player.location = render.DEATH
            actor.new_player()
        player.isInCombat = False
        render.HISTORY.append(
            "You manage to get away, taking %s damage." % damage_taken
        )
    else:
        damage_taken = monster.dealDamage(player)
        player.takeDamage(damage_taken)
        render.HISTORY.append("You fail to run away, taking %s damage." % damage_taken)
        if (player.hitpoints) <= 0:
            player.isInCombat = False
            player.location = render.DEATH
            actor.new_player()


def combat_encounter(player):
    roll = random.randint(0, 100)
    if roll >= 90:
        monster = actor.spawn_monster()
        player.location = render.DWARF
    elif roll >= 10:
        monster = actor.spawn_monster()
        player.location = render.DWARF
    else:
        monster = actor.spawn_monster()
        monster.takeDamage(monster.hitpoints * 0.3)
        player.location = render.DRUNKEN_DWARF
    # make monster range go from player level -2 to +2

    player.isInCombat = True
    render.HISTORY.append(
        "You encounter a level %i" % monster.level + " %s!" % monster.name
    )
    # combat(player, monster)


def random_encounter(self):
    roll = random.randint(0, 100)
    if roll > 90:
        self.location = render.EMPTY_PIC
        render.HISTORY.append("You find a boon. Your max HP is increased by 10 %.")

        self.maxHP = math.ceil(self.maxHP * 1.1)
        self.healHP(self.maxHP)
        return
    elif roll > 70:
        self.location = render.TREASURE_CHEST
        item = random.choice(items.item_pool)
        render.HISTORY.append("You found a treasure chest with a %s." % item.name)
        self.addItem(item)

    else:
        combat_encounter(self)


def boss_fight(player, boss):
    while player.isInCombat:
        x = input("What would you like to do?\n1. Attack\n2. Items\n")
        if x == "1":
            attack_boss(player, boss)
        elif x == "2":
            player.useItem()


def attack_boss(player, boss):
    dmg = player.dealDamage(boss)
    dmg_mob = boss.dealDamage(player)

    render.HISTORY.append("The %s" % boss.name + " deals %i damage." % dmg_mob)
    boss.takeDamage(dmg)
    render.HISTORY.append(
        "You strike the %s" % boss.name
        + " and deal %i damage." % dmg
        + " It has %i hitpoints left." % boss.hitpoints
    )
    if boss.hitpoints <= 0:
        render.HISTORY.append(
            "You slay the %s" % boss.name + " and gain %i EXP" % boss.experience
        )
        player.addExperience(boss.experience)

        player.gold += boss.gold
        boss_drop = random.choice(boss.dropTable)
        player.addItem(boss_drop)
        render.HISTORY.append("You find a %s." % boss_drop.name)

        render.HISTORY.append("You find %i gold." % boss.gold)

        del boss
        player.location = render.TREASURE_CHEST
        player.isInCombat = False
        player.counter = 0
    else:
        player.takeDamage(dmg_mob)
    if player.hitpoints <= 0:
        player.isInCombat = False
        player.location = render.DEATH
        # actor.new_player()
