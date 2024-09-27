from enum import Enum

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
    CHESTPLATE = 3
    HELMET = 4
    PANTS = 5
    RING = 6
    NECKLACE = 7

broken_dagger = Equipment('broken stone dagger', AP=1, DP=0, rarity=1,slot=ItemSlot.WEAPON)

weapon = [broken_dagger]

item_pool = weapon
