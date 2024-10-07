from enum import Enum

class Consumable:
    def __init__(self, name:str, damage:int, heal_mod:int, rarity:int):
        self.name = name
        self.rarity = rarity
        self.damage = damage
        self.heal = heal_mod*5+10
        self.value = 10 + 5*heal_mod + self.damage*5

class Equipment:
    def __init__(self, name:str, AP:int, DP:int, rarity:int, slot:Enum, description:str="Test item"):
        self.name = name
        self.rarity = rarity
        self.AP = AP
        self.DP = DP
        self.value = 30 + AP*9 + rarity*10 + DP*12
        self.slot = slot
        self.description = description

class ItemSlot(Enum):
    WEAPON = 1
    SHIELD = 2
    ARMOR = 3
    HELMET = 4
    BOOTS = 5
    RING = 6
    NECKLACE = 7
    TWO_HANDED_WEAPON = 8 # fix later (how 2h weapons are handled)

club        = Equipment(name='Club', AP=2, DP=0, rarity=1, slot=ItemSlot.WEAPON, description="A big wooden Club")
dagger      = Equipment(name='Dagger', AP=3, DP=0, rarity=2, slot=ItemSlot.WEAPON, description="A short pointy Dagger")
sword       = Equipment(name='Sword', AP=5, DP=3, rarity=4, slot=ItemSlot.WEAPON, description="A regular Sword")
shield      = Equipment(name='Bronze Shield', AP=0, DP=4, rarity=4, slot=ItemSlot.SHIELD, description="A round Shield")
sword_2       = Equipment(name='Heavy Sword', AP=10, DP=3, rarity=14, slot=ItemSlot.WEAPON, description="A very very Heavy Sword")
sword_3       = Equipment(name='Short Sword', AP=6, DP=1, rarity=5, slot=ItemSlot.WEAPON, description="A short and fast Sword")


helmet      = Equipment(name='Helmet',AP=0, DP=2, rarity=3, slot=ItemSlot.HELMET)
armor       = Equipment(name='Armor',AP=0, DP=4, rarity=3, slot=ItemSlot.ARMOR)
boots       = Equipment(name='Boots',AP=0, DP=3, rarity=3, slot=ItemSlot.BOOTS)

ring        = Equipment(name='Rusted ring', DP=1, AP=2, rarity=9, slot=ItemSlot.RING)
necklace    = Equipment(name='Old necklace', AP=2, DP=3, rarity=10, slot=ItemSlot.NECKLACE)

scroll      = Consumable(name='Old scroll', damage=1, heal_mod=0, rarity=1)
red_potion  = Consumable(name='Red Potion (L)', heal_mod=6, damage=0, rarity=7)
red_heal    = Consumable(name='Red potion (M)', heal_mod=2, damage=0, rarity=6)
big_heal    = Consumable(name='Red potion (XL)', heal_mod=10, damage=0, rarity=8)

accessory = [ring, necklace]
weapons = [club, dagger, sword, shield, sword_2]
armors = [helmet, armor, boots]
potion = [red_potion, red_heal, big_heal] * 2

item_pool = weapons + armors + potion + accessory