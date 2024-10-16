import random
import render
import items


def displayItems(items):
    count = 0
    for i in items:
        render.HISTORY.append(
            "%i. " % int(count + 1) + i.name + " - " + str(i.value) + " gold"
        )
        count += 1


def generateItems():
    wares = []
    for i in range(5):
        wares.append(random.choice(items.item_pool))
    return wares


def sellItem(player, slot):
    # for i in range(player.getInventorySize()):
    #     render.HISTORY.append(f"{i}. {player.inventory[i].name}")
    if player.getInventorySize() == 0:
        render.HISTORY.append("You have nothing to sell!")
        return
    try:
        player.gold += player.showInventory()[slot].value
    except ValueError as e:
        print(e)
        return
    render.HISTORY.append(
        "You sold a %s" % player.showInventory()[slot].name
        + " for %i gold." % player.showInventory()[slot].value
    )
    player.remItem(slot)


def buyItem(player, items, current_row):
    if len(player.inventory) == player.inventorySlots:
        render.HISTORY.append("Your bag is full.")
        return
    #     # check if weapon or potion
    #     i = input("Enter the number of the item\n")
    #     render.HISTORY.append(items[int(i) - 1].name)
    #     render.HISTORY.append("AP: " + str(items[int(i) - 1].AP))
    #     render.HISTORY.append("DP: " + str(items[int(i) - 1].DP))
    #     render.HISTORY.append("description: " + items[int(i) - 1].description)
    if player.gold < items[current_row].value:
        render.HISTORY.append(
            f"You do not have enough money to buy {items[current_row].name}."
        )
        return
    player.gold -= items[current_row].value
    player.addItem(items[current_row])
    render.HISTORY.append(f"You bought {items[current_row].name}")
    items.pop(current_row)
