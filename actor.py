import random

import render
import items
import combat


class Actor:
    def __init__(self, name="NULL", level=100):
        self.name = name
        self.level = level
        self.AP = level * 2 + 5
        self.DP = level * 2 + 5
        self.experience = level * 5
        self.hitpoints = 15 + level * 5
        self.maxHP = 15 + level * 5

    def takeDamage(self, amount):
        self.hitpoints -= amount
        if self.hitpoints <= 0:
            self.hitpoints = 0

    def dealDamage(self, target):
        dmg = random.randint(self.AP + 2 - target.DP, self.AP + 6 - target.DP)
        if dmg < 0:
            dmg = 0
        return dmg

    def healHP(self, amount):
        self.hitpoints += amount
        if self.hitpoints > self.maxHP:
            self.hitpoints = self.maxHP
        render.HISTORY.append(
            f"{self.name} heals for {amount}, and has now {self.hitpoints}."
        )


class Monster(Actor):
    def __init__(self, name, level, dropTable, picture):
        super().__init__(name, level)
        self.dropTable = dropTable
        self.picture = picture
        self.gold = random.randrange(3 * self.level, 10 * self.level)


class Boss(Actor):
    def __init__(self, name, level, dropTable, picture):
        super().__init__(name, level)
        self.dropTable = dropTable
        self.picture = picture
        self.gold = random.randrange(3 * self.level, 10 * self.level)


class Player(Actor):
    def __init__(
        self,
        name="player",
        level=1,
        inventory=[],
        experience=0,
        stamina=100,
        equipment={1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None},
        counter=0,
        dungen=1,
        location=render.EMPTY_PIC,
        gold=0,
        AP=3,
        DP=3,
    ):
        super().__init__(name, level)
        self.name = name
        self.AP = AP
        self.DP = DP
        self.level = level
        self.inventory = inventory
        self.location = location
        self.experience = experience
        self.isPlay = 1
        self.stamina = stamina
        self.inventorySlots = 18
        self.gold = gold
        self.equipment = equipment
        self.isInCombat = False
        self.counter = counter
        self.dungen = dungen

    def getStats(self):
        stats = [
            self.hitpoints,
            self.level,
            self.AP,
            self.DP,
            self.gold,
            self.experience,
            self.stamina,
        ]
        return stats

    # def getSaveStat(self):
    #     stats = self.getStats()
    #     stats.append(self.inventory)
    #     stats.append(self.equipment)
    #     return stats

    def saveGame(self):
        template = [
            "hitpoints",
            "level",
            "AP",
            "DP",
            "gold",
            "experience",
            "stamina",
            "inventory",
            " equipped",
        ]
        with open("savegame", "w") as save:
            for i, stat in enumerate(self.getStats()):
                stat = str(stat)
                save.write(stat)

    def getInventorySize(self):
        return len(self.inventory)

    def showInventory(self):
        return self.inventory

    def remItem(self, slot):
        self.inventory.pop(slot)

    def addItem(self, item):
        if len(self.inventory) == self.inventorySlots:
            render.HISTORY.append("Bag is full.")
            return
        self.inventory.append(item)
        # render.display_inventory()

    def useItem(self, item_slot):
        if len(self.inventory) == 0:
            render.HISTORY.append("Your inventory is empty.")
            return

        try:
            potion = self.inventory[int(item_slot) - 1].name
            heal = self.inventory[int(item_slot) - 1].healpower

            self.healHP(heal)
            render.HISTORY.append(
                "You use a %s potion " % potion + ", healing %i." % heal
            )
            self.remItem(int(item_slot) - 1)
        except:
            return
        return

    def scavenge(self):
        if self.stamina < 20:
            render.HISTORY.append("You have too little stamina.")
            self.moveTo(render.EMPTY_PIC)
            return
        roll = round(random.randint(0, 100))

        if roll > 90:
            self.stamina -= 20
            self.moveTo(render.TREASURE_CHEST)
            item = random.choice(items.item_pool)
            render.HISTORY.append("You found a treasure chest with a %s." % item.name)
            self.addItem(item)

        elif roll > 60:
            render.HISTORY.append("You find a merchant inside the dungeon!")
            self.location = render.SHOP
            # shop.shopMenu(self)
            return
        elif roll > 20:
            self.stamina -= 20
            self.moveTo(render.EMPTY_PIC)
            gold_amt = random.randint(0, 20)
            self.gold += gold_amt
            render.HISTORY.append("You found a %i gold pieces." % gold_amt)

        elif roll > 5:
            self.stamina -= 20
            self.moveTo(render.EMPTY_PIC)
            render.HISTORY.append("You found nothing.")
        else:
            combat.combat_encounter(self)

    def hunt(self):
        if self.stamina < 5:
            render.HISTORY.append("You have too little stamina.")
            self.moveTo(render.EMPTY_PIC)
            return
        self.stamina -= 5
        combat.random_encounter(self)

    def moveTo(self, location):
        self.location = location

    def die(self):
        # doesnt work
        self.moveTo(render.DEATH)
        render.HISTORY.append("You have died.")

        del self

    def addExperience(self, amount):
        self.counter += 1
        self.experience += amount
        if self.experience >= 10 + self.level**1.75:
            self.levelUp()
            render.HISTORY.append(
                "You gain a level. You are now level %i." % self.level
            )

    def getCurrentGold(self):
        return self.gold

    def levelUp(self):
        self.experience = 0
        self.level += 1
        self.AP += 2
        self.DP += 2
        self.maxHP += 5
        self.hitpoints = self.maxHP

    def rest(self):
        self.moveTo(render.FIRE)
        self.stamina = 100
        self.hitpoints = self.maxHP
        render.HISTORY.append("You are fully healed.")

    def equipItem(self, invSlot):
        try:
            slot_nr = self.showInventory()[invSlot].slot
            if slot_nr == 8:
                self.equipment.pop(0)
                self.equipment.pop(1)
            self.equipment[slot_nr] = self.showInventory()[invSlot]
        except:
            render.HISTORY.append(
                f"You can not equip {self.showInventory()[invSlot].name}"
            )
            return
        tot_AP = 0
        tot_DP = 0
        for k, v in self.equipment.items():
            if v:
                tot_AP += v.AP
                tot_DP += v.DP
        self.AP = tot_AP + self.level + 5
        self.DP = tot_DP + self.level + 2
        self.remItem(invSlot)
        render.HISTORY.append("You equip a %s." % self.equipment[slot_nr].name)

    def viewEquipment(self):
        equipment = [item[1].name for item in self.equipment.items() if item[1]]
        render.HISTORY.append("Items equipped: " + str(equipment))


GOBLIN = {
    "name": "Goblin",
    "level": random.randrange(1, 4),
    "dropTable": items.goblin_droptable,
    "picture": render.DWARF,
}
DRUNKEN_DWARF = {
    "name": "Dwarf",
    "level": random.randrange(1, 2),
    "dropTable": items.dwarf_droptable,
    "picture": render.DRUNKEN_DWARF,
}
DWARF = {
    "name": "Dwarf",
    "level": random.randrange(3, 6),
    "dropTable": items.dwarf_droptable,
    "picture": render.DWARF,
}
ORC = {
    "name": "Orc",
    "level": random.randrange(3, 6),
    "dropTable": items.dwarf_droptable,
    "picture": render.DWARF,
}
NECROMANCER = {
    "name": "Necromancer",
    "level": random.randrange(14, 16),
    "dropTable": items.dragon_sword,
    "picture": render.DWARF,
}
LIZARD = {
    "name": "Lizard",
    "level": random.randrange(5, 16),
    "dropTable": items.dragon_sword,
    "picture": render.DWARF,
}
DRAGON = {
    "name": "Dragon",
    "level": random.randrange(10, 16),
    "dropTable": items.dragon_sword,
    "picture": render.DWARF,
}

MONSTERS = [GOBLIN, DWARF, ORC, DRUNKEN_DWARF]
BOSSES = [DRAGON, NECROMANCER, LIZARD]


def spawn_monster():
    monster = random.choice(MONSTERS)
    monster = Monster(
        monster["name"], monster["level"], monster["dropTable"], monster["picture"]
    )
    return monster


def spawn_boss():
    boss = random.choice(BOSSES)
    boss = Boss(boss["name"], boss["level"], boss["dropTable"], boss["picture"])
    return boss
