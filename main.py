import os
import sys
import time


def mode():
    try:
        x = int(input(f"computer: 1{os.linesep}"
                      f"two player: 2{os.linesep}"
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


def mode_1():
    pass


def mode_2():
    pass


def mode_3():
    pass


game_mode = mode()

match game_mode:
    case 1:
        mode_1()
    case 2:
        mode_2()
    case 3:
        mode_3()
