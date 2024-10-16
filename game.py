import curses
import sys
import math
import actor
import render


class Game:
    def __init__(self):
        self.player = actor.Player()


def initialize(stdscr):
    curses.curs_set(0)
    render.init_colors()
    game = Game()
    run(stdscr, game.player)


def run(stdscr, player):
    while True:
        main_menu(stdscr, player)
        del player
        game = Game()
        player = game.player

        key = stdscr.getch()
        if key == ord("q"):
            break


def load_game(stdscr):
    f = open("savegame", "r")
    data = f.readlines()
    return render.render(stdscr, actor.Player(data))


def main_menu(stdscr, player):
    current_row = 0
    menu = ["Start Game", "Load Game", "Instructions", "Exit"]

    while True:
        stdscr.clear()

        # Get screen dimensions
        height, width = stdscr.getmaxyx()

        # Calculate start positions
        ascii_y_start = max((height - len(render.MENU_ART)) // 4, 0)
        menu_y_start = ascii_y_start + len(render.MENU_ART) + 3

        # Adjust if ASCII art is too tall for the screen
        visible_art = render.MENU_ART[: max(height - menu_y_start, 0)]
        if not visible_art:
            visible_art = render.MENU_ART[:]

        # Center the ASCII art
        for i, line in enumerate(visible_art):
            try:
                stdscr.addstr(ascii_y_start + i, (width - len(line)) // 2, line)
            except curses.error:
                pass

        # Draw a border around the menu
        border_padding = 2
        border_width = max(len(row) for row in menu) + border_padding * 2
        border_x_start = (width - border_width) // 2

        for i in range(len(menu) + 4):
            if i == 0 or i == len(menu) + 3:
                try:
                    stdscr.addstr(
                        menu_y_start + i,
                        border_x_start,
                        "+" + "-" * (border_width - 2) + "+",
                    )
                except curses.error:
                    pass
            else:
                try:
                    stdscr.addstr(menu_y_start + i, border_x_start, "|")
                    stdscr.addstr(
                        menu_y_start + i, border_x_start + border_width - 1, "|"
                    )
                except curses.error:
                    pass

        # Print the menu options centered within the border
        for idx, row in enumerate(menu):
            x = border_x_start + border_padding
            y = menu_y_start + 2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                try:
                    stdscr.addstr(y, x, row.center(border_width - border_padding * 2))
                except curses.error:
                    pass
                stdscr.attroff(curses.color_pair(1))
            else:
                try:
                    stdscr.addstr(y, x, row.center(border_width - border_padding * 2))
                except curses.error:
                    pass

        key = stdscr.getch()

        if (key == curses.KEY_UP or key == ord("k")) and current_row > 0:
            current_row -= 1
        elif (key == curses.KEY_DOWN or key == ord("j")) and current_row < len(
            menu
        ) - 1:
            current_row += 1
        elif key == ord("q"):
            sys.exit()
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            if current_row == 0:
                # Start game
                return render.render(stdscr, player)
            elif current_row == 1:
                load_game(stdscr)
            elif current_row == 2:
                show_instructions(stdscr)
            elif current_row == 3:
                sys.exit()

        stdscr.refresh()


def show_instructions(stdscr):
    screen_height, screen_width = stdscr.getmaxyx()
    stdscr.clear()
    for idx, line in enumerate(render.INSTRUCTIONS):
        try:
            stdscr.addstr(
                idx + math.floor(screen_height / 2),
                math.floor(screen_width / 2 - len(line) / 2),
                line,
            )
        except curses.error:
            pass
    stdscr.getch()  # Wait for any key press
