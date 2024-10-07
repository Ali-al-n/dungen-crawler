#!/bin/python3

import random
import os

import log
import canvas
import items
import actor

def displayItems(items):
    count = 0
    for i in items:
        log.history.append('%i. ' %int(count+1) + i.name + ' - ' + str(i.value)+ ' gold')
        count += 1
    canvas.canvas()

def generateItems():
    wares = []
    for i in range(5):
        wares.append(random.choice(items.item_pool))
    return wares

def sellItem(player):
    canvas.canvas()
    if player.getInventorySize() == 0:
           log.history.append('You have nothing to sell.')
           print('You have nothing to sell.')
           return
    try:
         x = int(input("Sell what?\n"))
    except ValueError as e:
        print(e)
        return
    try:
        player.gold += player.showInventory()[x-1].value
    except ValueError as e:
        print(e)
        return
    log.history.append('You sold a %s' %player.showInventory()[x-1].name + ' for %i gold.' % player.showInventory()[x-1].value)
    player.remItem(x-1)
    canvas.canvas()
def  buyItem(player, items):
    if len(items) == 0:
        log.history.append('There are no more items to buy.')
        return
    if player.getInventorySize() == 5:
        log.history.append('Your bag is full.')
        #ask if want to replace
        return
    y = input("What would you like to do?\n1. Buy\n2. Go Back\n3. Inspect Item\n")
    if y == "2":
        return
    elif y == "3":
        # check if weapon or potion
        i = input("Enter the number of the item\n" )
        log.history.append(items[int(i) - 1].name )
        log.history.append("AP: " + str(items[int(i) - 1].AP))
        log.history.append("DP: " + str(items[int(i) - 1].DP))
        log.history.append("description: " + items[int(i) - 1].description)
    elif y == "1":
        canvas.canvas()
        log.clear_history()
        try:
            x = int(input("Buy what?\n"))
        except ValueError as e:
            print(e)
            return
        if player.gold < items[x-1].value:
            canvas.canvas()
            print('You do not have enough money.')
            buyItem(player, items)
            return
        player.gold -= items[x-1].value
        player.addItem(items[x-1])
        items.pop(x-1)
        canvas.canvas()

# does not remove bought item
def shopMenu(player):
    items = generateItems()
    while True:
        canvas.canvas()
        x = input('What would you like to do?\n1. Browse wares\n2. Sell\n3. Leave shop\n')
        if x == "1":
            log.clear_history()
            displayItems(items)
            buyItem(player, items)
            #canvas.canvas()
            continue
        if x == "2":
            sellItem(player)
        if x == "3":
            log.clear_history()
            break
        else:
            pass

if __name__ == '__main__':
    actor.player1.gold = 1000
    for i in range(4):
        actor.player1.addItem(random.choice(items.item_pool))
    canvas.canvas()
    while True:
        shopMenu(actor.player1)

