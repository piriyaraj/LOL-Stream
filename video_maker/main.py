# -*- coding: utf-8 -*-
import time
from urllib.parse import unquote
import os
import subprocess
from usecases.get_run_command import get_commands
import subprocess

from usecases.game_controller import ControlGamePlay

if not os.path.exists("media/gameplay"):
    os.makedirs("media/gameplay")
if not os.path.exists("../playerLinks.txt"):
    with open("../playerLinks.txt","w") as player:
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

    playerTeam, playerIndex, driver, no_of_played_game = get_commands(playerLink, playerName, driver, playerTeam, playerIndex, no_of_played_game)
    if playerTeam != "None":
        gameController = ControlGamePlay(playerTeam,playerIndex)
        gameController.control()
        
if __name__ == "__main__":
    count = 0
    with open("../playerLinks.txt", "r") as file:
        playerLinks = file.readlines()
    while True:
        playerLink = playerLinks[count%len(playerLinks)].strip()
        count += 1
        if(count == len(playerLinks)):
            count = 0
        Run(playerLink)
        time.sleep(3*60)