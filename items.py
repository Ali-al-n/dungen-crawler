from enum import Enum

class Consumable:
    def __init__(self, name:str, damage:int, heal:int, rarity:int):
        self.name = name
        self.rarity = rarity
        self.damage = damage
        self.heal = heal*5+10
        self.value = 10 + 5*heal + self.damage*5

class Equipment:
    def __init__(self, name:str, AP:int, DP:int, rarity:int, slot:Enum):
        self.name = name
        self.rarity = rarity
        self.AP = AP
        self.DP = DP
        self.value = 30 + AP*9 + rarity*10 + DP*12
        self.slot = slot

class ItemSlot(Enum):
    WEAPON = 1
    SHIELD = 2
    ARMOR = 3
    HELMET = 4
    BOOTS = 5
    RING = 6
    NECKLACE = 7

club        = Equipment(name='Club', AP=1, DP=0, rarity=1, slot=ItemSlot.WEAPON)
dagger      = Equipment(name='Dagger', AP=2, DP=2, rarity=2, slot=ItemSlot.WEAPON)
sword       = Equipment(name='Rusted Sword', AP=4, DP=0, rarity=4, slot=ItemSlot.WEAPON)
shield      = Equipment(name='Bronze Shield', AP=0, DP=4, rarity=4, slot=ItemSlot.SHIELD)

helmet      = Equipment(name='Helmet',AP=0, DP=2, rarity=3, slot=ItemSlot.HELMET)
armor       = Equipment(name='Armor',AP=0, DP=4, rarity=3, slot=ItemSlot.ARMOR)
boots       = Equipment(name='Boots',AP=0, DP=3, rarity=3, slot=ItemSlot.BOOTS)

ring        = Equipment(name='Rusted ring', DP=0, AP=1, rarity=9, slot=ItemSlot.RING)
necklace    = Equipment(name='Old necklace', AP=1, DP=1, rarity=9, slot=ItemSlot.NECKLACE)

scroll      = Consumable(name='Old scroll', damage=1, heal=0, rarity=1)
red_potion  = Consumable(name='Red Potion (M)', heal=3, damage=0, rarity=6)
red_heal    = Consumable(name='Red potion (S)', heal=1, damage=0, rarity=6)

accessory = [ring, necklace]
weapons = [club, dagger, sword, shield]
armors = [helmet, armor, boots]
potion = [red_potion, red_heal] * 2

item_pool = weapons + armors + potion + accessory
