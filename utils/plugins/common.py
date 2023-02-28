
import os, sys
from time import sleep
from os import system, name
from pystyle import Colorate, Colors, Center

#    Saturn was proudly coded by wrxyut (https://github.com/wrxyut).
#    Copyright (c) 2022 wrxyut.
#    Saturn under the GNU GENERAL PUBLIC LICENSE Version3 (2007).


def clear():

    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')

def SlowPrint(_str):
    for letter in _str:
        sys.stdout.write(letter); sys.stdout.flush(); sleep(0.04)
    print()

def setTitle(_str):
    if name == 'nt':
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(f"{_str} | Made By Curelight")

    elif name == 'Linux':
        print(f"\033]0;{_str} | Made By Curelight\007", end='', flush=True)

def printCredit(_str):
    print(f"#    Saturn was proudly coded by {_str} (https://github.com/{_str}).")
    print(f"#    Copyright (c) 2022 {_str}.")
    print(f"#    Saturn under the GNU GENERAL PUBLIC LICENSE Version3 (2007).")

def pause():
    if name == 'nt':
        os.system('pause')
    elif name == 'Linux':
        os.system('sleep 5')


def fire(text):
    os.system(""); fade = ""
    green = 250
    for line in text.splitlines():
        fade += (f"\033[38;2;255;{green};0m{line}\033[0m\n")
        if not green == 0:
            green -= 25
            if green < 0:
                green = 0
    return fade

def banner():

    # Terminal 
    # Windows Size
    # Width 120 x height 30

    title = fire(f"""
                                                                                                _.u[[/;:,.         .odMM
                                                                                             .o888UU[[[/;:-.  .o@P^    M
                                                                                            oN88888UU[[[/;::-.        dP
                                                                                           dNMMNN888UU[[[/;:--.   .o@P^
                                                                                          ,MMMMMMN888UU[[/;::-. o@^
                                  ███████╗ █████╗ ████████╗██╗   ██╗██████╗ ███╗   ██╗    NNMMMNN888UU[[[/~.o@P^
                                  ██╔════╝██╔══██╗╚══██╔══╝██║   ██║██╔══██╗████╗  ██║    888888888UU[[[/o@^-..
                                  ███████╗███████║   ██║   ██║   ██║██████╔╝██╔██╗ ██║   oI8888UU[[[/o@P^:--..
                                  ╚════██║██╔══██║   ██║   ██║   ██║██╔══██╗██║╚██╗██║.@^  YUU[[[/o@^;::---..
    > Created by Wrxyut#0880      ███████║██║  ██║   ██║   ╚██████╔╝██║  ██║██║ ╚████║     ^/o@P^;:::---..
    > Running with python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}  ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝    .o@^ ^;::---...
                                                                                dMMMMMMM@^`       `^^^^
                                                                                YMMMUP^
    Warning: Some files may need to be fixed manually in order to work properly.  """)

    if name == "nt":
        print(title)
        print("────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
        print("────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\n")
    else:
        print("Saturn Skin Generator Made by Curelight (wrxyut)")