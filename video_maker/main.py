# -*- coding: utf-8 -*-
import time
from urllib.parse import unquote
import os
from usecases.get_run_command import get_commands

from usecases.game_controller import ControlGamePlay

import time
import pygetwindow as gw

from usecases.get_run_command import changePlayedGame


def closeGame():
    target_window_title = "league of legends (TM) client"

    # Get a list of all open windows
    open_windows = gw.getWindowsWithTitle(target_window_title)

    if open_windows:
        while True:
            print(f"{target_window_title} is open.")
            # Close the window

            open_windows = gw.getWindowsWithTitle(target_window_title)
            if open_windows:
                open_windows[0].close()
                print(f"{target_window_title} has been closed.")
                time.sleep(5)
                continue
            else:
                break
    else:
        print(f"{target_window_title} is not open.")


if not os.path.exists("media/gameplay"):
    os.makedirs("media/gameplay")
if not os.path.exists("media/screenshot"):
    os.makedirs("media/screenshot")
if not os.path.exists("../playerLinks.txt"):
    with open("../playerLinks.txt", "w") as player:
        pass

driver = None


def Run(playerLink):
    global driver
    playerLink = unquote(playerLink, encoding='utf-8')
    # playerLink = "https://www.op.gg/summoners/kr/쪼잔하게 굴지마/ingame"
    playerName = playerLink.split("/")[-2]
    print(f"====> {playerName} <====")

    playerTeam = None
    playerIndex = None
    no_of_played_game = None

    playerTeam, playerIndex, driver, no_of_played_game = get_commands(
        playerLink, playerName, driver, playerTeam, playerIndex, no_of_played_game)
    # playerTeam, playerIndex, driver, no_of_played_game = "Red",1,driver, 3
    if playerTeam != "None" and playerTeam != "Not found":
        time.sleep(1*60)
        
        gameController = ControlGamePlay(playerTeam, playerIndex)
        out = gameController.control()
        if out == "crashed":
            changePlayedGame()
    elif playerTeam == "Not found":
        pass
    else:
        driver = None
        closeGame()
        pass


if __name__ == "__main__":
    count = 0
    with open("../playerLinks.txt", "r") as file:
        playerLinks = file.readlines()
    while True:
        playerLink = playerLinks[count % len(playerLinks)].strip()
        count += 1
        if (count == len(playerLinks)):
            count = 0
        try:
            Run(playerLink)
            
        except Exception as e:
            count -= 1
            print("Error:", str(e))
