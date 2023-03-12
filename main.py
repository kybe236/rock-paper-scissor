import os
import random
import sys
import time

random.random()


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

    except Exception as ex:
        print(f"error: {ex}", file=sys.stderr)
        mode()


mode()
