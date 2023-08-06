# -*- coding: utf-8 -*-
from urllib.parse import unquote
import os
import subprocess
from usecases.get_run_command import get_commands
import subprocess

from usecases.game_controller import ControlGamePlay

if not os.path.exists("media/gameplay"):
    os.makedirs("media/gameplay")

def Run():
    playerLink = input("Enter ingame player Link (EX:'https://www.op.gg/summoners/kr/참새크면비둘기/ingame'): ")
    playerLink = unquote(playerLink, encoding='utf-8')
    # playerLink = "https://www.op.gg/summoners/kr/쪼잔하게 굴지마/ingame"
    playerName = playerLink.split("/")[-2]
    # print(playerName)
    driver = None
    playerTeam = None
    playerIndex = None
    no_of_played_game = None

    while True:
        playerTeam, playerIndex, driver, no_of_played_game = get_commands(playerLink, playerName, driver, playerTeam, playerIndex, no_of_played_game)
        
        gameController = ControlGamePlay(playerTeam,playerIndex)
        gameController.control()
if __name__ == "__main__":
    Run()