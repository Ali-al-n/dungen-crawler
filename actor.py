from enum import Enum, auto
import sys
import random

import canvas
import items
import shop
import combat
import log

class PlayerState(Enum):
    CAMPFIRE = auto()
    COMBAT = auto()
    SHOP = auto()
    DEATH = auto()
    LOOT_TREASURE = auto()

class Actor:
   def __init__(self, name='NULL', level=100):
       self.name = name
       self.level = level
       self.AP = level*2 + 5
       self.DP = level*2 + 5
       self.experience = level * 5
       self.hitpoints = 15 + level * 5
       self.maxHP = 15 + level * 5
   def takeDamage(self, amount):
       self.hitpoints -= amount
       if self.hitpoints <= 0:
           self.hitpoints = 0
   def dealDamage(self, target):
       dmg = random.randint(self.AP+2-target.DP,self.AP+6-target.DP)
       if dmg < 0:
           dmg = 0
       return dmg
   def healHP(self, amount):
       self.hitpoints += amount
       if self.hitpoints > self.maxHP:
            self.hitpoints = self.maxHP

class Monster(Actor):
    def __init__(self, name, level):
       super().__init__(name, level)
       self.dropTable = items.item_pool
       self.gold = random.randrange(3*self.level,10*self.level)


class Boss(Actor):
    def __init__(self, name, level):
       super().__init__(name, level)
       self.dropTable = items.boss_item_pool
       self.gold = random.randrange(3*self.level,10*self.level)

class Player(Actor):
   def __init__(self, name, level):
       super().__init__(name, level)
       self.name = 'Player'
       self.AP = 3
       self.DP = 3
       self.level = 1
       self.inventory = []
       self.location = None
       self.experience = 0
       self.stamina = 100
       self.inventorySlots = 10
       self.gold = 0
       self.equipment = { 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}
       self.isInCombat = False
       self.counter = 5
       self.dungen = 1

   def getInventorySize(self):
       return len(self.inventory)

   def showInventory(self):
       return self.inventory

   def remItem(self, slot):
       self.inventory.pop(slot)

   def addItem(self, item):
       if len(self.inventory) > self.inventorySlots:
           log.history.append('Bag is full.')
           return
       self.inventory.insert(0,item)

   def useItem(self):
       if len(self.inventory) == 0:
           log.history.append('Your inventory is empty.')
           return
       canvas.canvas()
       x = input('Choose what to use.\n')
       try:
           potion = self.inventory[int(x)-1].name
           heal = self.inventory[int(x)-1].healpower
           canvas.canvas()
           self.healHP(heal)
           log.history.append('You use a %s potion '%potion + ', healing %i.' %heal)
           self.remItem(int(x)-1)
       except:
           return
       return

   def scavenge(self):
       if self.stamina < 40:
           log.history.append('You have too little stamina.')
           self.moveTo(canvas.EMPTY_PIC)
           return
       roll = round(random.randint(0,100))

       if roll > 90:
           #self.stamina -= 40
           self.moveTo(canvas.TREASURE_CHEST)
           item = random.choice(items.item_pool)
           log.history.append('You found a treasure chest with a %s.' % item.name)
           self.addItem(item)
           canvas.canvas()
       elif roll > 80:
           log.history.append('You find a merchant inside the dungeon!')
           self.moveTo(canvas.SHOP)
           shop.shopMenu(self)
           return
       elif roll > 60:
           #self.stamina -= 20
           self.moveTo(canvas.EMPTY_PIC)
           gold_amt = random.randint(0,20)
           self.gold += gold_amt
           log.history.append("You found a %i gold pieces." % gold_amt)
           canvas.canvas()
       elif roll > 10:
           #self.stamina -= 20
           self.moveTo(canvas.EMPTY_PIC)
           log.history.append("You found nothing.")
       else:
           combat.combat_encounter(self)

   def hunt(self):
       if self.stamina < 25:
           log.history.append('You have too little stamina.')
           self.moveTo(canvas.EMPTY_PIC)
           return
       #self.stamina -= 25
       combat.random_encounter(self)

   def moveTo(self, location):
       self.location = location

   def die(self):
       #doesnt work 
       self.moveTo(canvas.DEATH)
       log.history.append('You have died.')
       canvas.canvas()
       del self

   def addExperience(self, amount):
       self.counter += 1
       self.experience += amount
       if self.experience >= 10+self.level**1.75:
           self.levelUp()
           log.history.append('You gain a level. You are now level %i.' %self.level)

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
       self.moveTo(canvas.FIRE)
       self.stamina = 100
       self.hitpoints = (self.maxHP)
       log.history.append("You are fully healed.")

   def equipItem(self, invSlot):
       try:
           slot_nr = self.showInventory()[invSlot-1].slot
           if slot_nr == 8:
               self.equipment.pop(0)
               self.equipment.pop(1)
           self.equipment[slot_nr] = self.showInventory()[invSlot-1]
       except:
           return
       tot_AP = 0
       tot_DP = 0
       for k, v in self.equipment.items():
           if v:
               tot_AP += v.AP
               tot_DP += v.DP
       self.AP = tot_AP + self.level + 5
       self.DP = tot_DP + self.level + 2
       self.remItem(invSlot-1)
       log.history.append('You equip a %s.' %self.equipment[slot_nr].name)

   def viewEquipment(self):
       equipment = [item[1].name for item in self.equipment.items() if item[1]]
       log.history.append('Items equipped: ' + str(equipment))

   def play(self):
       if self:
           canvas.canvas()
           if self.counter >=  5:
               x = input("What would you like to do?\n1. Hunt\n2. Scavenge\n3. Rest\n4. Equip item\n5. View Equipment.\n6. Fight Boss")
           else:
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
           elif x =="6":
               boss = Boss("Ancient Dragon", 10)
               self.moveTo(canvas.DWARF)
               self.isInCombat = True
               combat.boss_fight(self, boss)
           else:
               pass
       else:
           #canvas.canvas()
               self.rest()

player1 = Player(name='Adventurer', level=1)

def new_player(name='Adventurer', level=1):
    if 'player1' not in locals() or 'player1' not in globals():
        log.history.append('You have died.')
        canvas.canvas()
        global player1
        x = input("What would you like to do?\n1. Play again\n2. Quit\n")
        if x == "1":
            player1 = Player(name, level)
            log.clear_history()
            canvas.canvas()
        else:
            sys.exit()
