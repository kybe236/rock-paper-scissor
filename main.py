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
    print(f"1: rock"
          f"2: paper"
          f"3. scissor")

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


def computer():
    pick_1 = random.randrange(1, 3)
    print(pick_1)


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
