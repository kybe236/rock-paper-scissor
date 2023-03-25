#!/usr/bin/env python
import getpass
import logging
import os
import random
import signal
import socket
import sys
import time
import requests


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
        case 4:
            web_server()


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


def user_pick(user: int) -> int:
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
                      f"server(socket): 3{os.linesep}"
                      f"public server: 4{os.linesep}"
                      f"enter number: "))

        if x not in (1, 2, 3, 4):
            logging.warning("number not in range")
            time.sleep(0.1)  # wait until stderr is printed
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


def compare(x: int, wins_player_1: int, wins_player_2: int) -> None:
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
        return input_server()


def get_server_ip() -> str:
    try:
        inp = str(input(f"domain: Url, IPv4, IPv6{os.linesep}"
                        f"enter domain: "))

        return inp
    except Exception as ex:
        logging.error(f"{ex}")
        return get_server_ip()


def connect_or_create():
    try:
        inp = int(input(f"create server: 1{os.linesep}"
                        f"connect server: 2{os.linesep}"
                        f"enter: "))
        if inp not in (1, 2):
            logging.error("number not in range")
            return connect_or_create()

        inp2 = int(input(f"server code: "))

        result = [inp, inp2]

        return result

    except Exception as ex:
        logging.debug(ex)
        return connect_or_create()


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

        compare(x, wins_player_1, wins_player_2)


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

        compare(x, pick_1, pick_2)


def computer():
    wins_player_1 = 0
    wins_player_2 = 0
    while (wins_player_1 < 3) and (wins_player_2 < 3):
        pick_1 = random.randrange(1, 3)
        pick_2 = user_pick(2)
        x = pick_compare(pick_1, pick_2)

        compare(x, pick_1, pick_2)


def multiplayer():
    wins_player_1 = 0
    wins_player_2 = 0
    while (wins_player_1 < 3) and (wins_player_2 < 3):
        pick_1 = user_pick(1)
        pick_2 = user_pick(2)
        x = pick_compare(pick_1, pick_2)

        compare(x, pick_1, pick_2)


def online():
    server_type = input_server()
    if server_type == 1:
        server()
    client()


def web_server():
    ip = get_server_ip()
    code_type, code = connect_or_create()
    player_1_wins = 0
    player_2_wins = 0
    token = random.randrange(99999999999)

    url = f"{ip}/{code}/?"

    first = True

    if code_type == 1:
        requests.get(f"{url}action=create")
        requests.get(f"{url}action=token&token={token}")
    else:
        requests.get(f"{url}action=token&token={token}")
    if code_type == 1:
        while (player_1_wins < 3) and (player_2_wins < 3):
            r = requests.get(f"{url}action=next")
            while r.json() == {'next': 2}:
                time.sleep(0.2)
                r = requests.get(f"{url}action=next")
            if first:
                first = False
            else:
                with requests.get(f"{url}action=last_winner") as w:  # noqa
                    w = w.json()
                    if w == {'last_winner': 0}:
                        print_with_sep("draw")
                    if w == {'last_winner': 1}:
                        print_with_sep("you won")
                        player_1_wins += 1
                    if w == {'last_winner': 2}:
                        print_with_sep("enemy won")
                        player_2_wins += 1
            if player_1_wins == 3:
                print_with_sep("you won the game")
                sys.exit(0)
            if player_2_wins == 3:
                print_with_sep("enemy won the game")
                sys.exit(0)
            pick = user_pick(1)
            requests.get(f"{url}action=play&token={token}&pick={pick}")

    if code_type == 2:
        while (player_1_wins < 3) and (player_2_wins < 3):
            r = requests.get(f"{url}action=next")
            while r.json() == {'next': 1}:
                time.sleep(0.2)
                r = requests.get(f"{url}action=next")
            pick = user_pick(2)
            requests.get(f"{url}action=play&token={token}&pick={pick}")
            with requests.get(f"{url}action=last_winner") as w:  # noqa
                w = w.json()
                if w == {'last_winner': 0}:
                    print_with_sep("draw")
                if w == {'last_winner': 1}:
                    print_with_sep("enemy won")
                    player_1_wins += 1
                if w == {'last_winner': 2}:
                    print_with_sep("you won")
                    player_2_wins += 1
            if player_1_wins == 3:
                print_with_sep("enemy won the game")
                sys.exit(0)
            if player_2_wins == 3:
                print_with_sep("you won the game")
                sys.exit(0)


main()
