import sys
import time
import getpass
import os
import socket
import asyncio


def pick_compare(player1: int, player2: int):
    match player1:
        case 1:  # rock
            match player2:
                case 1:
                    return 0
                case 2:
                    return 2
                case 3:
                    return 1
        case 2:  # paper
            match player2:
                case 1:
                    return 1
                case 2:
                    return 0
                case 3:
                    return 2
        case 3:  # scissors
            match player2:
                case 1:
                    return 2
                case 2:
                    return 1
                case 3:
                    return 0


def user_pick(user: int):
    print(f"1: rock{os.linesep}"
          f"2: paper{os.linesep}"
          f"3: scissor")

    try:
        x = int(getpass.getpass(f"player {user} : "))

        if x not in (1, 2, 3):
            print("error: number is not in range ", file=sys.stderr)
            time.sleep(0.1)  # wait until stderr is printed (maybe a bug)
            user_pick(user)

        return x

    except Exception as ex:
        print(f"error: {ex}", file=sys.stderr)
        user_pick(user)


def mode():
    try:
        x = int(input(f"computer: 1{os.linesep}"
                      f"multiplayer(2 player): 2{os.linesep}"
                      f"enter number: "))

        if x not in (1, 2):
            print("error: number is not in range ", file=sys.stderr)
            time.sleep(0.1)  # wait until stderr is printed (maybe a bug)
            mode()

        return x

    except Exception as ex:
        print(f"error: {ex}", file=sys.stderr)
        mode()


def print_with_sep(prin):
    print(os.linesep + prin + os.linesep)


