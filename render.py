import curses

import actor
import combat
import shop


def render(stdscr, player):
    render_screen(stdscr, player)
    if player.isInCombat:
        combat_menu(stdscr, player)
    elif player.location == SHOP:
        render_shop_menu(stdscr, player)
    elif player.location == EQUIP_ITEM:
        equip_item_menu(stdscr, player)
    else:
        game_menu(stdscr, player)

    draw_player_stats(stdscr, player)
    game_messages(stdscr, player)


def render_screen(stdscr, player):
    stdscr.clear()
    draw_player_location(stdscr, player)
    draw_player_stats(stdscr, player)
    display_inventory(stdscr, player)
    game_messages(stdscr, player)


def draw_player_stats(stdscr, player):
    stats = player.getStats()
    separator = "######################"
    stdscr.addstr(0, len(player.location[0]), separator)
    for idy, line in enumerate(STATUS_WINDOW):
        stdscr.addstr(idy + 1, len(player.location[0]), line + str(stats[idy]))
    stdscr.addstr(len(STATUS_WINDOW) + 1, len(player.location[0]), separator)


def use_item(stdscr, player):
    # current_row = 0
    stdscr.addstr(len(STATUS_WINDOW) + 1, len(player.location[0]), " Inventory:")
    for idy, item in enumerate(player.inventory):
        stdscr.addstr(
            len(STATUS_WINDOW) + 2 + idy,
            len(player.location[0]) + 1,
            str(str(idy + 1) + ". " + item.name),
        )


def display_inventory(stdscr, player):
    stdscr.addstr(len(STATUS_WINDOW) + 2, len(player.location[0]), " Inventory:")
    for idy, item in enumerate(player.inventory):
        stdscr.addstr(
            len(STATUS_WINDOW) + 3 + idy,
            len(player.location[0]) + 1,
            str(str(idy + 1) + ". " + item.name),
        )


def render_shop_sell_menu(stdscr, player):
    current_row = 0
    q = "What would you like to sell?"
    while True:
        stdscr.addstr(len(EMPTY_PIC) + len(MSG_BOX) + 1, 0, q)
        for idy, line in enumerate(player.inventory):
            if idy == current_row:
                stdscr.attron(curses.color_pair(1))
                try:
                    stdscr.addstr(
                        len(player.location) + len(MSG_BOX) + idy + 2,
                        0,
                        str(idy + 1) + ". " + line.name,
                    )
                except curses.error:
                    pass
                stdscr.attroff(curses.color_pair(1))
            else:
                try:
                    stdscr.addstr(
                        len(player.location) + len(MSG_BOX) + idy + 2,
                        0,
                        str(idy + 1) + ". " + line.name,
                    )
                except curses.error:
                    pass
        stdscr.refresh()

        key = stdscr.getch()

        if (key == curses.KEY_UP or key == ord("k")) and current_row > 0:
            current_row -= 1
        elif (
            key == curses.KEY_DOWN or key == ord("j")
        ) and current_row < player.getInventorySize() - 1:
            current_row += 1
        elif key == ord("q"):
            render_screen(stdscr, player)
            break
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            shop.sellItem(player, current_row)
            current_row = 0

        render_screen(stdscr, player)


def render_shop_buy_menu(stdscr, player, items):
    current_row = 0
    q = "What would you like to buy?"
    while True:
        stdscr.addstr(len(EMPTY_PIC) + len(MSG_BOX) + 1, 0, q)
        for idy, line in enumerate(items):
            if idy == current_row:
                stdscr.attron(curses.color_pair(1))
                try:
                    stdscr.addstr(
                        len(player.location) + len(MSG_BOX) + idy + 2,
                        0,
                        str(idy + 1) + ". " + line.name,
                    )
                except curses.error:
                    pass
                stdscr.attroff(curses.color_pair(1))
            else:
                try:
                    stdscr.addstr(
                        len(player.location) + len(MSG_BOX) + idy + 2,
                        0,
                        str(idy + 1) + ". " + line.name,
                    )
                except curses.error:
                    pass
        stdscr.refresh()

        key = stdscr.getch()

        if (key == curses.KEY_UP or key == ord("k")) and current_row > 0:
            current_row -= 1
        elif (key == curses.KEY_DOWN or key == ord("j")) and current_row < len(
            items
        ) - 1:
            current_row += 1
        elif key == ord("q"):
            render_screen(stdscr, player)
            break
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            shop.buyItem(player, items, current_row)
            stdscr.clear()
            render_screen(stdscr, player)
            break
            if current_row == 2:
                inspect_item()

        draw_player_location(stdscr, player)
        draw_player_stats(stdscr, player)
        game_messages(stdscr, player)


def inspect_item(stdscr, player):
    pass


def render_shop_menu(stdscr, player):
    current_row = 0
    items = shop.generateItems()
    stdscr.clear()
    render_screen(stdscr, player)
    while player.location == SHOP:
        shop_menu = "You are in a Shop. What would you like to do?"
        stdscr.addstr(len(EMPTY_PIC) + len(MSG_BOX) + 1, 0, shop_menu)
        for idy, line in enumerate(SHOP_MENU):
            if idy == current_row:
                stdscr.attron(curses.color_pair(1))
                try:
                    stdscr.addstr(
                        len(player.location) + len(MSG_BOX) + idy + 2, 0, line
                    )
                except curses.error:
                    pass
                stdscr.attroff(curses.color_pair(1))
            else:
                try:
                    stdscr.addstr(
                        len(player.location) + len(MSG_BOX) + 2 + idy, 0, line
                    )
                except curses.error:
                    pass

        stdscr.refresh()

        key = stdscr.getch()

        if (key == curses.KEY_UP or key == ord("k")) and current_row > 0:
            current_row -= 1
        elif (key == curses.KEY_DOWN or key == ord("j")) and current_row < len(
            SHOP_MENU
        ) - 1:
            current_row += 1
        elif key == ord("q"):
            player.location = EMPTY_PIC
            render_screen(stdscr, player)
            break
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            if current_row == 0:
                # Buy
                render_screen(stdscr, player)
                render_shop_buy_menu(stdscr, player, items)
                # shop.
            elif current_row == 1:
                # Sell
                render_shop_sell_menu(stdscr, player)
            elif current_row == 2:
                # Leave
                HISTORY.append("You leave the shop")
                player.location = EMPTY_PIC
                stdscr.clear()
                render_screen(stdscr, player)
        draw_player_location(stdscr, player)
        draw_player_stats(stdscr, player)
        game_messages(stdscr, player)


def combat_menu(stdscr, player):
    current_row = 0
    monster = actor.spawn_monster()
    while player.isInCombat:
        menu_str = "What would you like to do?"
        stdscr.addstr(len(player.location) + len(MSG_BOX) + 1, 0, menu_str)
        for idy, line in enumerate(COMBAT_MENU_OPTIONS):
            if idy == current_row:
                stdscr.attron(curses.color_pair(1))
                try:
                    stdscr.addstr(
                        len(player.location) + len(MSG_BOX) + idy + 1, 0, line
                    )
                except curses.error:
                    pass
                stdscr.attroff(curses.color_pair(1))
            else:
                try:
                    stdscr.addstr(
                        len(player.location) + len(MSG_BOX) + 1 + idy, 0, line
                    )
                except curses.error:
                    pass

        stdscr.refresh()

        key = stdscr.getch()

        if (key == curses.KEY_UP or key == ord("k")) and current_row > 0:
            current_row -= 1
        elif (key == curses.KEY_DOWN or key == ord("j")) and current_row < len(
            COMBAT_MENU_OPTIONS
        ) - 1:
            current_row += 1
        elif key == ord("q"):
            stdscr.addstr(
                len(player.location) + len(COMBAT_MENU_OPTIONS) + len(MSG_BOX) + 2,
                0,
                "Quitting is disabled during battles!",
            )
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            if current_row == 0:
                # Attack
                # monster = actor.spawn_monster()
                combat.attack(player, monster)
                render_screen(stdscr, player)
                pass
            elif current_row == 1:
                # Items
                use_item_menu(stdscr, player)
                render_screen(stdscr, player)
            elif current_row == 2:
                # Run
                combat.run(player, monster)
                render_screen(stdscr, player)
                pass
            elif current_row == 3:
                pass
        draw_player_location(stdscr, player)
        draw_player_stats(stdscr, player)
        game_messages(stdscr, player)


def use_item_menu(stdscr, player):
    current_row = 0
    player_is_selecting = 1
    while player_is_selecting:
        menu_str = "What would you like to do?"
        stdscr.addstr(len(player.location) + len(MSG_BOX), 0, menu_str)
        for idy, line in enumerate(player.inventory):
            if idy == current_row:
                stdscr.attron(curses.color_pair(1))
                try:
                    stdscr.addstr(
                        len(player.location) + len(MSG_BOX) + idy + 1, 0, line.name
                    )
                except curses.error:
                    pass
                stdscr.attroff(curses.color_pair(1))
            else:
                try:
                    stdscr.addstr(
                        len(player.location) + len(MSG_BOX) + 1 + idy, 0, line.name
                    )
                except curses.error:
                    pass

        stdscr.refresh()

        key = stdscr.getch()

        if (key == curses.KEY_UP or key == ord("k")) and current_row > 0:
            current_row -= 1
        elif (key == curses.KEY_DOWN or key == ord("j")) and current_row < len(
            player.inventory
        ) - 1:
            current_row += 1
        elif key == ord("q"):
            break
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            player.useItem(current_row)
            render_screen(stdscr, player)


def draw_player_location(stdscr, player):
    for idy, line in enumerate(player.location):
        stdscr.addstr(idy, 0, line)


def equip_item_menu(stdscr, player):
    current_row = 0
    render_screen(stdscr, player)
    draw_player_location(stdscr, player)
    while player.location == EQUIP_ITEM:
        menu_str = "What would you like to equip?"
        stdscr.addstr(len(player.location) + 1 + len(MSG_BOX), 0, menu_str)
        for idx in range(player.getInventorySize()):
            # x = border_x_start + border_padding
            # y = menu_y_start + 2 + idx

            # paint selected option red
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                try:
                    stdscr.addstr(
                        1 + len(player.location) + len(MSG_BOX) + idx + 1,
                        0,
                        str(idx + 1) + ". " + player.inventory[idx].name,
                    )
                except curses.error:
                    pass
                stdscr.attroff(curses.color_pair(1))
            else:
                try:
                    stdscr.addstr(
                        1 + len(player.location) + len(MSG_BOX) + idx + 1,
                        0,
                        str(idx + 1) + ". " + player.inventory[idx].name,
                    )
                except curses.error:
                    pass

        stdscr.refresh()

        # Grab player input
        key = stdscr.getch()

        if key == ord("q"):
            player.location = EMPTY_PIC
            render(stdscr, player)
            break
        stdscr.addstr(
            len(player.location) + len(GAME_MENU_OPTIONS) + len(MSG_BOX) + 2,
            0,
            "                                     ",
        )
        if (key == curses.KEY_UP or key == ord("k")) and current_row > 0:
            current_row -= 1
        elif (
            key == curses.KEY_DOWN or key == ord("j")
        ) and current_row < player.getInventorySize() - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            player.equipItem(current_row)
            player.location = EMPTY_PIC
        # draw_player_location(stdscr, player)
        # draw_player_stats(stdscr, player)
        # game_messages(stdscr, player)


def game_menu(stdscr, player):
    current_row = 0
    if player.counter > 5:
        menu = GAME_MENU_OPTIONS_BOSS
        y = len(player.location) + len(MSG_BOX) + 2
    else:
        menu = GAME_MENU_OPTIONS
        y = len(player.location) + len(MSG_BOX) + 2
    while player.isPlay:
        menu_str = "What would you like to do?"
        stdscr.addstr(y - 1, 0, menu_str)
        for idx, row in enumerate(menu):
            # paint selected option red
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                try:
                    stdscr.addstr(y + idx, 0, row)
                except curses.error:
                    pass
                stdscr.attroff(curses.color_pair(1))
            else:
                try:
                    stdscr.addstr(y + idx, 0, row)
                except curses.error:
                    pass

        stdscr.refresh()

        # Grab player input
        key = stdscr.getch()

        if key == ord("q"):
            stdscr.addstr(
                len(player.location) + len(menu) + len(MSG_BOX) + 2,
                0,
                "Are you sure? (press Q again to quit)",
            )
            key = stdscr.getch()
            if key == ord("q"):
                player.saveGame()
                player.isPlay = 0
                stdscr.clear()
                stdscr.addstr(
                    len(player.location) + len(menu) + len(MSG_BOX) + 2,
                    0,
                    "Press any key to return to main menu.",
                )
                break
        stdscr.addstr(
            len(player.location) + len(menu) + len(MSG_BOX) + 2,
            0,
            "                                                                 ",
        )
        if (key == curses.KEY_UP or key == ord("k")) and current_row > 0:
            current_row -= 1
        elif (key == curses.KEY_DOWN or key == ord("j")) and current_row < len(
            menu
        ) - 1:
            current_row += 1

        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            if current_row == 0:
                # Start game
                player.hunt()
            elif current_row == 1:
                # Scavenge
                player.scavenge()
                render(stdscr, player)
            elif current_row == 2:
                # Rest
                player.rest()
            elif current_row == 3:
                # Equip Item
                if player.getInventorySize() == 0:
                    HISTORY.append("Your inventory is empty.")
                else:
                    player.location = EQUIP_ITEM
                    equip_item_menu(stdscr, player)
                    # break
                render(stdscr, player)
            elif current_row == 4:
                # View Equipment
                player.viewEquipment()
            elif current_row == 5:
                # Boss fight
                boss_fight_menu(stdscr, player)
                render(stdscr, player)
            render(stdscr, player)


def boss_fight_menu(stdscr, player):
    current_row = 0
    monster = actor.spawn_boss()
    while player.isInCombat:
        menu_str = "What would you like to do?"
        stdscr.addstr(len(player.location) + len(MSG_BOX) + 1, 0, menu_str)
        for idy, line in enumerate(COMBAT_MENU_OPTIONS):
            if idy == current_row:
                stdscr.attron(curses.color_pair(1))
                try:
                    stdscr.addstr(
                        len(player.location) + len(MSG_BOX) + idy + 1, 0, line
                    )
                except curses.error:
                    pass
                stdscr.attroff(curses.color_pair(1))
            else:
                try:
                    stdscr.addstr(
                        len(player.location) + len(MSG_BOX) + 1 + idy, 0, line
                    )
                except curses.error:
                    pass

        stdscr.refresh()

        key = stdscr.getch()

        if (key == curses.KEY_UP or key == ord("k")) and current_row > 0:
            current_row -= 1
        elif (key == curses.KEY_DOWN or key == ord("j")) and current_row < len(
            COMBAT_MENU_OPTIONS
        ) - 1:
            current_row += 1
        elif key == ord("q"):
            stdscr.addstr(
                len(player.location) + len(COMBAT_MENU_OPTIONS) + len(MSG_BOX) + 2,
                0,
                "Quitting is disabled during battles!",
            )
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            if current_row == 0:
                # Attack
                # monster = actor.spawn_monster()
                combat.attack(player, monster)
                render_screen(stdscr, player)
                pass
            elif current_row == 1:
                # Items
                use_item_menu(stdscr, player)
                render_screen(stdscr, player)
            elif current_row == 2:
                # Run
                combat.run(player, monster)
                render_screen(stdscr, player)
                pass
            elif current_row == 3:
                pass
        draw_player_location(stdscr, player)
        draw_player_stats(stdscr, player)
        game_messages(stdscr, player)


def game_messages(stdscr, player):
    MSG_BOX = HISTORY[-LOG_SIZE:]
    for idx, line in enumerate(MSG_BOX):
        stdscr.addstr(len(player.location) + idx, 0, " " * 50)
        stdscr.addstr(len(player.location) + idx, 0, line)
    stdscr.addstr(len(player.location) + len(MSG_BOX), 0, SEPARATOR)


def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)


EMPTY_PIC = [
    "##################################################################",
    "#               |                 |             |                #",
    "#_______________|_________________|_____________|________________#",
    "#       |               |               |               |        #",
    "#_______|_______________|_______________|_______________|________#",
    "#               |                 |             |                #",
    "#_______________|_________________|_____________|________________#",
    "#       |               |               |               |        #",
    "#_______|_______________|_______________|_______________|________#",
    "#               |                 |             |                #",
    "#_______________|_________________|_____________|________________#",
    "#       |               |               |               |        #",
    "#_______|_______________|_______________|_______________|________#",
    "#               |                 |             |                #",
    "#_______________|_________________|_____________|________________#",
    "#       |               |               |               |        #",
    "#_______|_______________|_______________|_______________|________#",
    "#               |                 |             |                #",
    "#_______________|_________________|_____________|________________#",
    "#       |               |               |               |        #",
    "#_______|_______________|_______________|_______________|________#",
    "#__/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_#",
    "#_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/____#",
    "#__/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_#",
    "#_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/____#",
    "#__/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_#",
    "#_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/____#",
    "#__/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_#",
    "##################################################################",
]
TREASURE_CHEST = [
    "##################################################################",
    "#       |               |               |               |        #",
    "#_______|_______________|_______________|_______________|________#",
    "#               |                 |             |                #",
    "#_______________|_________________|_____________|________________#",
    "#       |               |               |               |        #",
    '#_______|____________.=""_;=.___________|_______________|________#',
    '#|              | ,-" _,=""  `"=. |             |                #',
    '#|______________|_"=._o`"-._     `"=.___________|________________#',
    '#       |             `"=._o`"=._   _`"=._              |        #',
    '#_______|__________________:=._o "=._."_.-="""=.________|________#',
    '#|              |   __.--" , ; `"=._o." ,-"""-._ ".              #',
    '#|______________|._"  ,. .` ` `` ,  `"-._"-._ ". " `_____________#',
    '#       |        |o`"=._` , "` `; .". ,  "-._"-._; ;    |        #',
    '#_______|________| ;`-.o`"=._; ." ` "`."`` . "-._ /_____|________#',
    '#               ||o;    `"-.o`"=._`` "` " ,__.--o;               #',
    '#_______________|| ;    (#) `-.o `"=.`_.--"_o.-; ;_______________#',
    '#_____/_____/____|o;._          `".o|o_.--"    ;o;_____/_____/___#',
    '#/_____/_____/_____"=._o--._      ; | ;        ; ;___/_____/_____#',
    '#___/_____/_____/_____/"=._o--._  ;o|o;     _._;o;____/_____/____#',
    '#_/_____/_____/_____/______"=._o._; | ;_.--"o.--"_/_____/_____/__#',
    '#____/_____/_____/_____/_____/__"=.o|o_.--""___/_____/_____/_____#',
    "#__/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_#",
    "#_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/____#",
    "#__/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_#",
    "#_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/____#",
    "#__/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_#",
    "#_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/____#",
    "##################################################################",
]
FIRE = [
    "##################################################################",
    "#       |               |               |               |        #",
    "#_______|_______________|_______________|_______________|________#",
    "#               |                 |             |                #",
    "#_______________|_________________|_____________|________________#",
    "#       |               |               |               |        #",
    "#_______|_______________|_______________|_______________|________#",
    "#               |                 |             |                #",
    "#_______________|_________⣀_______|⣄⠀___________|________________#",
    "#       |               |⢸⣿⡄  ⡀   ⢸⣿⣷⡄⠀⠀|⠀⠀⠀            |        #",
    "#_______|_______________|_⢿⠇__⣷⣦⣤⣴⣿⣿⣿⣷__|_______________|________#",
    "#               |    ⠀⠀⠀⠀⡀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀     |                #",
    "#_______________|_______⣾⣷⡀__⣸⣿⣿⣿⣿⣿⣿⣿⠃__________|________________#",
    "# /_____/_____/____/__⢰⣿⣿⣿⣿⣷⣿⣿⣿⡟⢿⠿⠋⣿⣿⠀___⠰⣄⠀____/_____/_____/____#",
    "# ____/_____/_____/____⣾⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⣿⣿⣦⡀__⢀⣿⣧_____/_____/_____/__#",
    "# /____/_____/_____/__⢹⣿⣿⣿⠙⠻⠟⠋⠁⠀⠀⠀⠀⢿⣿⣿⣿⣶⣶⣿⣿⣿__/_____/_____/_____/#",
    "# _____/_____/_____/__⠈⣿⣿⣿⡆⠀⠀⢀⣠⡤⠀⠀⠀⠈⠻⣿⡿⣿⣿⣿⣿⡟_____/_____/_____/___#",
    "# _____/_____/____/____⠘⠟⠋⣁⣤⡾⢟⣩⣴⣶⣆⠀⠀⠀⠀⢠⣿⣿⣿⠟⠀__/_____/_____/_____/#",
    "# ___/_____/_____/____⢀⣠⣴⣿⣿⣿⣿⠟⢉⣁⣀⣉⠀⢹⣶⣶⣤⣄⣈⡁⠀/_____/_____/_____/___#",
    "# _____/_____/____/__⢸⣿⣿⣿⣿⢿⣿⠇⢰⡟⣫⣦⠙⢷⡀⣿⣿⣯⣍⣛⠛⠋___/_____/_____/_____/#",
    "# __/_____/_____/____⠀⠛⢋⣡⡾⠟⠋⠀⠸⣧⣙⡟⢁⡾⠁⠿⢿⣿⣿⣭⡉⠁/_____/_____/_____/___#",
    "# ____/_____/_____/_____/_____/⠙⠛⠋____/⠈⠉⠉_____/_____/_____/____/#",
    "#__/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_#",
    "#_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/____#",
    "#__/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_#",
    "#_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/____#",
    "#__/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_#",
    "#_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/____#",
    "##################################################################",
]
DWARF = [
    "##################################################################",
    "#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣿⢿⣟⣾⣽⣿⣻⢿⣿⢿⣶⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠟⣟⣛⡻⠛⠛⠻⣿⣿⢯⡿⣽⢯⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⡎⡄⢰⠠⣔⣂⡁⠀⠘⡎⡱⢉⠫⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢿⣿⣇⣿⣿⣿⣟⢛⣆⣰⡠⢔⣆⢄⣸⣣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⣹⠁⢿⡌⡛⠛⠈⣽⣿⣿⣞⢎⣿⣿⣿⡦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣵⣵⣦⣷⣼⣮⣂⣾⣿⡟⣯⣋⣶⢩⠛⣳⡳⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀⠀⠀⠀⢀⣤⠤⢀⠀⠀⡠⠢⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⡐⠩⣾⢿⣿⡷⠒⣻⣝⣿⣯⣿⡷⡾⣮⡡⠚⠉⠀⣈⡵⠂⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀⠀⠀⠀⢿⢗⠢⣀⣨⣦⣠⢡⠃⠀⠀⠀⠀⠀⠀⠀⠀⡴⠋⠽⣿⣿⣻⣟⣿⡿⣿⣿⢷⣿⣏⡠⠊⠀⠀⡠⢮⢀⡼⠞⠻⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀⠀⠀⠀⠀⡑⡢⢽⣟⡶⢯⣋⠉⠂⢄⣀⡀⠄⣀⠀⢀⠟⠒⢠⠞⠛⢿⡾⢿⣿⣯⣿⢻⢇⡘⠀⠀⠠⣊⢠⡾⠋⠀⠀⢀⡿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀⠀⠀⠀⢜⠌⢀⣄⠀⠙⠯⣀⢹⡞⢧⡄⢚⡑⠮⡃⠜⣄⢀⣸⣂⣐⣾⣾⣿⣧⠍⣀⠀⢎⣑⠂⢰⡁⡤⣾⠬⠭⠍⡩⠥⣇⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀⠀⢀⢮⠊⣠⠟⠀⡜⢀⢪⠊⡙⢠⠇⣸⠋⣵⠲⢉⠴⣉⠁⡆⢀⠠⢼⡿⣿⡏⠁⠒⠨⠕⢋⣷⣶⣎⣮⡀⠀⠀⡤⠀⠒⠘⡥⠣⡀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀⢠⡣⠁⢴⡋⠀⠐⠀⢢⠃⠀⠙⢧⣄⠁⠸⠃⣼⣃⠀⠀⠉⠒⠥⡒⢨⠁⠂⢿⡐⣄⡀⠀⡸⣼⣯⠟⣫⣻⠭⠭⠭⠍⡒⢴⡡⣹⠃⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#_/_⣰⠟⣮⡢⡀⠙⠳⡆⠘⡸⡀____⠛⠻⠤⠶⠗⠋⠐⢤⣀⠀⠀⠉⠢⢄⡀⠈⠛⠦⠽⠞⣿⢖⠌⡈⠑⠒⠄⡀⠀⠈⡣⣿__/_____/_____#",
    "#____⠻⡦⣛⢦⣕⠄⡀⠀⠐⠹⣢⠤⣞⡢⣄_____/_⣽⢷⡦⣄⡀⠠⢈⠐⠠⢤⣤⡞⢩⠯⠯⢮⣔⢄⠀⠈⣦⠾⠋_/_____/_____/_#",
    "#__/___⠛⢾⣄⣻⣚⡵⣂⣤⡴⣬⣖⡽⣏⣿⠆_/___⣯⣟⣟⣾⣿⣷⣦⣈⠐⡄⡩⠉⠫⢠⡞⢘⡲⢝⣺⣶⠇_____/______/____#",
    "#_____/___⠛⠷⢿⣼⣧⣽⣵⣯⡾⠟_____/⡰⠃⣬⠫⢻⣝⢝⣿⢿⡿⢶⡽⣏⠀⡌⠈⡙⠣⣾⢿⡉___/______/_____/_#",
    "#_____/_____/____/____/__⡴⢋⡙⠢⠥⠦⠭⢗⣦⣽⣾⣍⡑⠠⢛⠻⣴⣷⠚⠀⠩⣷_/_____/_____/____#",
    "#__/_____/_____/_____/__⠼⣲⡒⠦⠓⣾⠋⣙⣉⣟⣽⠊⠹⣽⢭⣠⣁⣢⢟⣢⢄⣿⣞⠆____/_____/_____/#",
    "#_____/_____/_____/_____⡕⠒⠒⠈⡇⡿⠶⡦⠛⠋⣉⠆_⢏⣓⣏⠀⠨⠭⠔⠊⣎⣯⡇_/_____/_____/___#",
    "#_/_____/_____/_____/____⢢⠤⢐⡵⠉⠑⡬⢶⣿⡏__⠸⣅⡛⢜⠄⣀⣀⢔⡹⢂⢻____/_____/_____/#",
    "#____/_____/_____/_____/__⢫⢇⠀⠀⠀⢱⠛⡍⡀_/_⢸⡗⡇⠁⠒⢲⠉⠀⠀⡇⢃_/_____/_____/__#",
    "#_/_____/_____/_____/_____⢀⡫⠤⠤⢀⢸⠴⣿⣿_/__⢻⣱⡀⠀⠀⣇⣀⣀⣟⣺____/_____/_____#",
    "#_____/_____/_____/____/_⠒⠁⠀⠀⠀⠀⢹⣽⠛⠉⡆__/_⠻⣗⡔⠉⠀⠀⠈⢻⣇_/_____/_____/__#",
    "#__/_____/_____/_____/_⡸⠤⢔⣂⠤⢀⣀⢴⣿⣿⣗⡦⢳⣶⣶⣶⣶⣶⡾⡇⠀⠀⠀⠀⢎⣫⣦⣄⣀/_____/____/_#",
    "#____/_____/_____⣠⣤⣶⣾⣿⣿⣇⡀⠀⠀⠉⠑⠊⢡⡻⣷⣿⣶⣿⣿⣿⣿⣿⣿⣇⠃⢐⣒⣀⡜⣲⣋⣼⣿⣿⣿⣿⣿⣷⣶⣦⣄⡀_/___#",
    "#__/_____/_____/⣿⣿⣿⣿⣿⣿⣿⣟⠚⠷⢒⣖⣲⡮⠝⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉⠈⠀⠀⠀⠈⣵⢊⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆____#",
    "#____/_____/____⠙⠿⢿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡙⠳⠶⠒⠖⠲⠯⠗⢋⣼⣿⣿⣿⣿⣿⣿⡿⠿⠋__/__#",
    "##################################################################",
]
DRUNKEN_DWARF = [
    "##################################################################",
    "#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣿⢿⣟⣾⣽⣿⣻⢿⣿⢿⣶⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠟⣟⣛⡻⠛⠛⠻⣿⣿⢯⡿⣽⢯⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⡎⡄⢰⠠⣔⣂⡁⠀⠘⡎⡱⢉⠫⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀           ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢿⣿⣇⣿⣿⣿⣟⢛⣆⣰⡠⢔⣆⢄⣸⣣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀           ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⣹⠁⢿⡌⡛⠛⠈⣽⣿⣿⣞⢎⣿⣿⣿⡦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀             ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣵⣵⣦⣷⣼⣮⣂⣾⣿⡟⣯⣋⣶⢩⠛⣳⡳⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀             ⠀⠀⠀⠀⠀⠀⠀⠀⡐⠩⣾⢿⣿⡷⠒⣻⣝⣿⣯⣿⡷⡾⣮⡡⠚⠉⠀⣈⡵⠂⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀             ⠀⠀⠀⠀⠀⠀⠀⡴⠋⠽⣿⣿⣻⣟⣿⡿⣿⣿⢷⣿⣏⡠⠊⠀⠀⡠⢮⢀⡼⠞⠻⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀             ⢄⣀⡀⠄⣀⠀⢀⠟⠒⢠⠞⠛⢿⡾⢿⣿⣯⣿⢻⢇⡘⠀⠀⠠⣊⢠⡾⠋⠀⠀⢀⡿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀           ⢹⡞⢧⡄⢚⡑⠮⡃⠜⣄⢀⣸⣂⣐⣾⣾⣿⣧⠍⣀⠀⢎⣑⠂⢰⡁⡤⣾⠬⠭⠍⡩⠥⣇⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀           ⡙⢠⠇⣸⠋⣵⠲⢉⠴⣉⠁⡆⢀⠠⢼⡿⣿⡏⠁⠒⠨⠕⢋⣷⣶⣎⣮⡀⠀⠀⡤⠀⠒⠘⡥⠣⡀⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#⠀⠀⠀⠀           ⠙⢧⣄⠁⠸⠃⣼⣃⠀⠀⠉⠒⠥⡒⢨⠁⠂⢿⡐⣄⡀⠀⡸⣼⣯⠟⣫⣻⠭⠭⠭⠍⡒⢴⡡⣹⠃⠀⠀⠀⠀⠀⠀⠀   ⠀ #",
    "#_____/_____/____/____⠶⠗⠋⠐⢤⣀⠀⠀⠉⠢⢄⡀⠈⠛⠦⠽⠞⣿⢖⠌⡈⠑⠒⠄⡀⠀⠈⡣⣿__/_____/_____#",
    "#__/_____/_____/_____/___/_⣽⢷⡦⣄⡀⠠⢈⠐⠠⢤⣤⡞⢩⠯⠯⢮⣔⢄⠀⠈⣦⠾⠋_/_____/_____/_#",
    "#_____/_____/_____/____/___⣯⣟⣟⣾⣿⣷⣦⣈⠐⡄⡩⠉⠫⢠⡞⢘⡲⢝⣺⣶⠇_____/______/____#",
    "#_/_____/_____/_____/____/⡰⠃⣬⠫⢻⣝⢝⣿⢿⡿⢶⡽⣏⠀⡌⠈⡙⠣⣾⢿⡉___/______/_____/_#",
    "#_____/_____/____/____/__⡴⢋⡙⠢⠥⠦⠭⢗⣦⣽⣾⣍⡑⠠⢛⠻⣴⣷⠚⠀⠩⣷_/_____/_____/____#",
    "#__/_____/_____/_____/__⠼⣲⡒⠦⠓⣾⠋⣙⣉⣟⣽⠊⠹⣽⢭⣠⣁⣢⢟⣢⢄⣿⣞⠆____/_____/_____/#",
    "#_____/_____/_____/_____⡕⠒⠒⠈⡇⡿⠶⡦⠛⠋⣉⠆_⢏⣓⣏⠀⠨⠭⠔⠊⣎⣯⡇_/_____/_____/___#",
    "#_/_____/_____/_____/____⢢⠤⢐⡵⠉⠑⡬⢶⣿⡏__⠸⣅⡛⢜⠄⣀⣀⢔⡹⢂⢻____/_____/_____/#",
    "#____/_____/_____/_____/__⢫⢇⠀⠀⠀⢱⠛⡍⡀_/_⢸⡗⡇⠁⠒⢲⠉⠀⠀⡇⢃_/_____/_____/__#",
    "#_/_____/_____/_____/_____⢀⡫⠤⠤⢀⢸⠴⣿⣿_/__⢻⣱⡀⠀⠀⣇⣀⣀⣟⣺____/_____/_____#",
    "#_____/_____/_____/____/_⠒⠁⠀⠀⠀⠀⢹⣽⠛⠉⡆__/_⠻⣗⡔⠉⠀⠀⠈⢻⣇_/_____/_____/__#",
    "#__/_____/_____/_____/_⡸⠤⢔⣂⠤⢀⣀⢴⣿⣿⣗⡦⢳⣶⣶⣶⣶⣶⡾⡇⠀⠀⠀⠀⢎⣫⣦⣄⣀/_____/____/_#",
    "#____/_____/_____⣠⣤⣶⣾⣿⣿⣇⡀⠀⠀⠉⠑⠊⢡⡻⣷⣿⣶⣿⣿⣿⣿⣿⣿⣇⠃⢐⣒⣀⡜⣲⣋⣼⣿⣿⣿⣿⣿⣷⣶⣦⣄⡀_/___#",
    "#__/_____/_____/⣿⣿⣿⣿⣿⣿⣿⣟⠚⠷⢒⣖⣲⡮⠝⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉⠈⠀⠀⠀⠈⣵⢊⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆____#",
    "#____/_____/____⠙⠿⢿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡙⠳⠶⠒⠖⠲⠯⠗⢋⣼⣿⣿⣿⣿⣿⣿⡿⠿⠋__/__#",
    "##################################################################",
]


DEATH = [
    "##################################################################",
    "#                    ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶                   #",
    "#_________________¶¶¶¶                       ¶¶¶¶________________#",
    "#                ¶¶¶                             ¶¶              #",
    "#_______________¶¶                                ¶¶_____________#",
    "#              ¶¶                                 ¶¶             #",
    "#_____________¶¶                                   ¶¶____________#",
    "#             ¶¶ ¶¶                             ¶¶ ¶¶            #",
    "#_____________¶¶ ¶¶                             ¶¶  ¶____________#",
    "#             ¶¶ ¶¶                             ¶¶  ¶            #",
    "#_____________¶¶  ¶¶                            ¶¶ ¶¶____________#",
    "#             ¶¶  ¶¶                           ¶¶  ¶¶            #",
    "#______________¶¶ ¶¶   ¶¶¶¶¶¶¶¶     ¶¶¶¶¶¶¶¶   ¶¶ ¶¶ ____________#",
    "#               ¶¶¶¶ ¶¶¶¶¶¶¶¶¶¶     ¶¶¶¶¶¶¶¶¶¶ ¶¶¶¶¶             #",
    "#________________¶¶¶ ¶¶¶¶¶¶¶¶¶¶     ¶¶¶¶¶¶¶¶¶¶ ¶¶¶   ____________#",
    "#       ¶¶¶       ¶¶  ¶¶¶¶¶¶¶¶       ¶¶¶¶¶¶¶¶¶  ¶¶      ¶¶¶¶     #",
    "#____ _¶¶¶¶¶_____¶¶   ¶¶¶¶¶¶¶   ¶¶¶   ¶¶¶¶¶¶¶   ¶¶_____¶¶¶¶¶¶  __#",
    "#     ¶¶   ¶¶    ¶¶     ¶¶¶    ¶¶¶¶¶    ¶¶¶     ¶¶    ¶¶   ¶¶    #",
    "#___ ¶¶¶    ¶¶¶¶  ¶¶          ¶¶¶¶¶¶¶          ¶¶  ¶¶¶¶    ¶¶¶ __#",
    "#   ¶¶         ¶¶¶¶¶¶¶¶       ¶¶¶¶¶¶¶       ¶¶¶¶¶¶¶¶¶        ¶¶  #",
    "#___¶¶¶¶¶¶¶¶¶     ¶¶¶¶¶¶¶¶    ¶¶¶¶¶¶¶    ¶¶¶¶¶¶¶¶      ¶¶¶¶¶¶¶¶__#",
    "#_/_  ¶¶¶¶ ¶¶¶¶¶      ¶¶¶¶¶              ¶¶¶ ¶¶     ¶¶¶¶¶¶ ¶¶¶ __#",
    "#_____________¶¶¶¶¶¶  ¶¶¶  ¶¶           ¶¶  ¶¶¶  ¶¶¶¶¶¶__/____/__#",
    "#_/____/_____/____¶¶¶¶¶¶ ¶¶ ¶¶¶¶¶¶¶¶¶¶¶ ¶¶ ¶¶¶¶¶¶_____/____/____/#",
    "#_____________________¶¶ ¶¶ ¶ ¶ ¶ ¶ ¶ ¶ ¶ ¶ ¶¶______/___/____/___#",
    "#_/__/___/__/_______¶¶¶¶  ¶ ¶ ¶ ¶ ¶ ¶ ¶ ¶   ¶¶¶¶¶____/____/____/_#",
    "#_______________¶¶¶¶¶ ¶¶   ¶¶¶¶¶¶¶¶¶¶¶¶¶   ¶¶ ¶¶¶¶¶______________#",
    "#_/_____¶¶¶¶¶¶¶¶¶¶_____¶¶_________________¶¶______¶¶¶¶¶¶¶¶¶    __#",
    "##################################################################",
]
SHOP = [
    "##################################################################",
    "#               |                 |             |                #",
    "#__________##############################################________#",
    "#       |  #                                            #        #",
    "#_______|__#                 DUNGEON SHOP               #________#",
    "#          #                                            #        #",
    "#__________##############################################________#",
    "#       |  |            |               |               |        #",
    "#_______|__|____________|_______________|_______________|________#",
    "#          |    |                 |             |       |        #",
    "#__________|____|_________________|_____________|_______|________#",
    "#       |  |            |               |               |        #",
    "#_______|__|____________|_______________|_______________|________#",
    "#          |    |                 |             |       |        #",
    "#__________|____________________________________________|________#",
    "#       |  /                                            |        #",
    "#_______|_/                                            /|________#",
    "#        /                                            /¶|        #",
    "#________#############################################¶¶|________#",
    "#       |#############################################¶¶|        #",
    "#_______|#############################################¶¶|________#",
    "#__/_____#############################################¶¶|/_____/_#",
    "#_____/__#############################################¶¶/___/____#",
    "#__/_____#############################################¶/_/_____/_#",
    "#_____/__#############################################/_____/____#",
    "#__/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_#",
    "#_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/____#",
    "#__/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_#",
    "##################################################################",
]
EQUIP_ITEM = [
    "##################################################################",
    "#               |                 |             |                #",
    "#____        &                        /(#          ______________#",
    "#            /%    #&              @ *(##             |          #",
    "#____       &&&%/@@&@@@@@@@@@@@@@@@@ *#%#%%&       ___|__________#",
    "#         &%((**,,(&%@@@@@@@@@@@@(&#,/*****/#(                   #",
    "#____    //*    .,*/**@@&@@@@@.#%(*/*,,.     #((   ______________#",
    "#       ,#       ,*/**@@&%%%%%%%@ //**,.     % *#     |          #",
    "#____  .# ,  .  , ///@##%%%&%%#(((&&/((/*. *@%**(  ___|__________#",
    "#       * ,#@ **.&%/ ./#%%%&%%#(/.  ...  .@ @@&*/@@              #",
    "#____(    ,@@%@&/     ,(/###%(##*       #&@        ______________#",
    "#           @% &(    , .%/#%%#(%*.*     ##@           |          #",
    "#____          %%*      ,(#%###(*.     /(%         ___|__________#",
    "#              %%#*    .,%%###% ,.    ,#%#                       #",
    "#____          #&(/(...*%%&%&%%%%*., .*%%#         ______________#",
    "#              %&#/,...,(%%%&&%%#/,...,#%(            |          #",
    "#____          *&#*/,,,*(%&&&&%%#( .,,*/%/         ___|__________#",
    "#              %&%(.   ,(&&&%###(.    (#%(                       #",
    "#____         %&##*/  .,(#%%%%%#(,  & ,/#@%        ______________#",
    "#            %&&/*.%..,/#%%%#%%#(/,.(,* @&%           |          #",
    "#__________  &&&&/..,/,(%%%&%%%#%&(*,..##@%#       ___|__________#",
    "#__/___/____&#@.....(#@,//     (%@@@  .,*@@&       ____/______/__#",
    "#___________(##/*,,,,,@%       .#@..( .*(%&((      _/_____/______#",
    "#__/___/___/*#(/,,.../%#        @&(.. .,(#%&%      ____/______/__#",
    "#__________(%#(/,,..*%/          @@*...,/#%%%      _/_____/______#",
    "#__/___/____##(*,,,(               #,#..,/##%      ____/______/__#",
    "#___________(%(((,%.                %%,.,*(#       _/_____/______#",
    "#__/___/___/__/((..                  / %%**        ____/______/__#",
    "##################################################################",
]
MENU_ART = [
    r" /$$$$$$$                                                                                  ",
    r"| $$__  $$                                                                                 ",
    r"| $$  \ $$ /$$   /$$ /$$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$$                      ",
    r"| $$  | $$| $$  | $$| $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$| $$__  $$                     ",
    r"| $$  | $$| $$  | $$| $$  \ $$| $$  \ $$| $$$$$$$$| $$  \ $$| $$  \ $$                     ",
    r"| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$_____/| $$  | $$| $$  | $$                     ",
    r"| $$$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$$|  $$$$$$$|  $$$$$$/| $$  | $$                     ",
    r"|_______/  \______/ |__/  |__/ \____  $$ \_______/ \______/ |__/  |__/                     ",
    r"                               /$$  \ $$                                                   ",
    r"                              |  $$$$$$/                                                   ",
    r"                               \______/                                                    ",
    r"                          /$$$$$$                                   /$$                    ",
    r"                         /$$__  $$                                 | $$                    ",
    r"                        | $$  \__/  /$$$$$$  /$$$$$$  /$$  /$$  /$$| $$  /$$$$$$   /$$$$$$ ",
    r"                        | $$       /$$__  $$|____  $$| $$ | $$ | $$| $$ /$$__  $$ /$$__  $$",
    r"                        | $$      | $$  \__/ /$$$$$$$| $$ | $$ | $$| $$| $$$$$$$$| $$  \__/",
    r"                        | $$    $$| $$      /$$__  $$| $$ | $$ | $$| $$| $$_____/| $$      ",
    r"                        |  $$$$$$/| $$     |  $$$$$$$|  $$$$$/$$$$/| $$|  $$$$$$$| $$      ",
    r"                         \______/ |__/      \_______/ \_____/\___/ |__/ \_______/|__/      ",
    r"                                                                                           ",
    r"                                                                                           ",
    r"                                                                                           ",
]
INSTRUCTIONS = [
    "Instructions:",
    "Navigate menus with H, J, K, L or Arrow Keys.",
    "Press Spacebar or Enter to confirm selected option.",
    "Press Q to quit the game.",
    "",
    "Press any key to return to the menu.",
]
GAME_MENU_OPTIONS_BOSS = [
    "1. Hunt",
    "2. Scavenge",
    "3. Rest",
    "4. Equip item",
    "5. View Equipment.",
    "6. Fight Boss",
]
GAME_MENU_OPTIONS = [
    "1. Hunt",
    "2. Scavenge",
    "3. Rest",
    "4. Equip item",
    "5. View Equipment.",
]
COMBAT_MENU_OPTIONS = ["1. Attack", "2. Items", "3. Run"]
STATUS_WINDOW = [
    " HP              : ",
    " Level           : ",
    " AP              : ",
    " DP              : ",
    " Gold            : ",
    " Experience      : ",
    " Stamina         : ",
]

SHOP_MENU = ["1. Browse wares", "2. Sell", "3. Leave shop"]
SHOP_BUY_MENU = ["1. Buy", "2. Go Back", "3. Inspect Item"]

HISTORY = ["", "", "", "", "", "", "", "", "", ""]
HISTORY_CLEAN = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
SEPARATOR = "###################################################################"
LOG_SIZE = 5

MSG_BOX = HISTORY[-LOG_SIZE:]
