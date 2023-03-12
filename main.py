import os
import random
import sys
import time


def mode():
    try:
        x = int(input(f"computer: 1{os.linesep}"
                      f"multiplayer: 2{os.linesep}"
                      f"online: 3{os.linesep}"
                      f"enter number: "))

        if x not in (1, 2, 3):
            print("error: number is not in range ", file=sys.stderr)
            time.sleep(0.1)  # wait until stderr is printed (maybe a bug)
            mode()

        return x

    except Exception as ex:
        print(f"error: {ex}", file=sys.stderr)
        mode()


def user_pick(user: int):
    print(f"1: rock{os.linesep}"
          f"2: paper{os.linesep}"
          f"3: scissor")

    try:
        x = int(input(f"player{user} : pick"))

        if x not in (1, 2, 3):
            print("error: number is not in range ", file=sys.stderr)
            time.sleep(0.1)  # wait until stderr is printed (maybe a bug)
            user_pick(user)

        return x

    except Exception as ex:
        print(f"error: {ex}", file=sys.stderr)
        user_pick(user)


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


def computer():
    wins_player_1 = 0
    wins_player_2 = 0
    while (wins_player_1 < 3) and (wins_player_2 < 3):
        pick_1 = random.randrange(1, 3)
        pick_2 = user_pick(2)
        x = pick_compare(pick_1, pick_2)

        if wins_player_1 == 3:
            print("bot wins")
        if wins_player_2 == 3:
            print("player wins")


def multiplayer():
    pass


def online():
    pass


game_mode = mode()

match game_mode:
    case 1:
        computer()
    case 2:
        multiplayer()
    case 3:
        online()
