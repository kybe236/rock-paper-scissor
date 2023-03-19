#!/usr/bin/env python
import getpass
import logging
import os
import random
import signal
import socket
import sys
import time


def main():
    signal.signal(signal.SIGINT, signal_handler)
    game_mode = mode()

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
            logging.warning("number not in range")
            time.sleep(0.1)  # wait until stderr is printed (maybe a bug)
            user_pick(user)

        return x

    except Exception as ex:
        logging.error(f"{ex}")
        user_pick(user)


def mode():
    try:
        x = int(input(f"computer: 1{os.linesep}"
                      f"multiplayer(2 player): 2{os.linesep}"
                      f"server: 3{os.linesep}"
                      f"enter number: "))

        if x not in (1, 2, 3):
            logging.warning("number not in range")
            time.sleep(0.1)  # wait until stderr is printed (maybe a bug)
            return mode()

        return x

    except Exception as ex:
        logging.error(f"{ex}")
        mode()


def ip_pick():
    return str(input("ip: "))


def print_with_sep(prin):
    print(os.linesep + prin + os.linesep)


def get_ipv6():
    return socket.getaddrinfo(socket.gethostname(), 1234, socket.AF_INET6)[0][4][0]


def input_server():
    try:
        inp = int(input(f"server: 1{os.linesep}"
                        f"connect: 2{os.linesep}"
                        f"select number: "))

        if inp not in (1, 2):
            logging.warning("number not in range")
            time.sleep(0.1)  # wait until stderr is printed (maybe a bug)
            return input_server()

        return inp

    except Exception as ex:
        logging.error(f"{ex}")
        input_server()


def server():
    print(f"{get_ipv6()}")
    ip = get_ipv6()
    ip = ip.strip()
    ser = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    ser.bind((ip, 1234))
    ser.listen()

    wins_player_1 = 0
    wins_player_2 = 0
    while (wins_player_1 < 3) and (wins_player_2 < 3):
        pick_1 = user_pick(1)
        client_c, addr = ser.accept()
        client_c.send(str(pick_1).encode())
        pick_2 = int(client_c.recv(1024).decode())

        x = pick_compare(pick_1, pick_2)

        if x == 0:
            print_with_sep("draw")
        if x == 1:
            print_with_sep("player 1")
            wins_player_1 += 1
        if x == 2:
            print_with_sep("player 2")
            wins_player_2 += 1

        if wins_player_1 == 3:
            print_with_sep("player 1 wins")
        if wins_player_2 == 3:
            print_with_sep("player 2 wins")


def client():
    ip = ip_pick()

    def connect_rec():
        try:
            client_soc = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            client_soc.connect((ip, 1234, 0, 0))

        except Exception as ex:
            logging.debug(f"loop: {ex}")
            time.sleep(0.1)
            return connect_rec()
        return client_soc

    wins_player_1 = 0
    wins_player_2 = 0
    while (wins_player_1 < 3) and (wins_player_2 < 3):
        client_sock = connect_rec()
        pick_1 = int(client_sock.recv(1024).decode())
        pick_2 = user_pick(2)
        client_sock.send(str(pick_2).encode())

        x = pick_compare(pick_1, pick_2)

        if x == 0:
            print_with_sep("draw")
        if x == 1:
            print_with_sep("player 1")
            wins_player_1 += 1
        if x == 2:
            print_with_sep("player 2")
            wins_player_2 += 1

        if wins_player_1 == 3:
            print_with_sep("player 1 wins")
        if wins_player_2 == 3:
            print_with_sep("player 2 wins")


def computer():
    wins_player_1 = 0
    wins_player_2 = 0
    while (wins_player_1 < 3) and (wins_player_2 < 3):
        pick_1 = random.randrange(1, 3)
        pick_2 = user_pick(2)
        x = pick_compare(pick_1, pick_2)

        if x == 0:
            print_with_sep("draw")
        if x == 1:
            print_with_sep("bot")
            wins_player_1 += 1
        if x == 2:
            print_with_sep("player 2")
            wins_player_2 += 1

        if wins_player_1 == 3:
            print_with_sep("bot wins")
        if wins_player_2 == 3:
            print_with_sep("player wins")


def multiplayer():
    wins_player_1 = 0
    wins_player_2 = 0
    while (wins_player_1 < 3) and (wins_player_2 < 3):
        pick_1 = user_pick(1)
        pick_2 = user_pick(2)
        x = pick_compare(pick_1, pick_2)

        if x == 0:
            print_with_sep("draw")
        if x == 1:
            print_with_sep("player 1")
            wins_player_1 += 1
        if x == 2:
            print_with_sep("player 2")
            wins_player_2 += 1

        if wins_player_1 == 3:
            print_with_sep("player 1 wins")
        if wins_player_2 == 3:
            print_with_sep("player 2 wins")


def online():
    server_type = input_server()
    if server_type == 1:
        server()
    client()


main()
