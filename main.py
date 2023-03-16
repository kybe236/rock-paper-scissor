import logging
import random
import signal
import sys

import lib


def main():
    signal.signal(signal.SIGINT, signal_handler)
    game_mode = lib.mode()

    match game_mode:
        case 1:
            computer()
        case 2:
            multiplayer()
        case 3:
            online()


def signal_handler(sign, frame):
    logging.debug(f"{sign} {frame}")
    sys.exit(0)


def computer():
    wins_player_1 = 0
    wins_player_2 = 0
    while (wins_player_1 < 3) and (wins_player_2 < 3):
        pick_1 = random.randrange(1, 3)
        pick_2 = lib.user_pick(2)
        x = lib.pick_compare(pick_1, pick_2)

        if x == 0:
            lib.print_with_sep("draw")
        if x == 1:
            lib.print_with_sep("bot")
            wins_player_1 += 1
        if x == 2:
            lib.print_with_sep("player 2")
            wins_player_2 += 1

        if wins_player_1 == 3:
            lib.print_with_sep("bot wins")
        if wins_player_2 == 3:
            lib.print_with_sep("player wins")


def multiplayer():
    wins_player_1 = 0
    wins_player_2 = 0
    while (wins_player_1 < 3) and (wins_player_2 < 3):
        pick_1 = lib.user_pick(1)
        pick_2 = lib.user_pick(2)
        x = lib.pick_compare(pick_1, pick_2)

        if x == 0:
            lib.print_with_sep("draw")
        if x == 1:
            lib.print_with_sep("player 1")
            wins_player_1 += 1
        if x == 2:
            lib.print_with_sep("player 2")
            wins_player_2 += 1

        if wins_player_1 == 3:
            lib.print_with_sep("player 1 wins")
        if wins_player_2 == 3:
            lib.print_with_sep("player 2 wins")


def online():
    server_type = lib.input_server()
    if server_type == 1:
        lib.server()
    else:
        lib.client()

main()