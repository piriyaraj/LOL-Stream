import os
import subprocess
from usecases.get_run_command import get_commands
import subprocess

from usecases.game_controller import ControlGamePlay

if not os.path.exists("media/gameplay"):
    os.makedirs("media/gameplay")


# playerLink = input("Enter ingame player Link (EX:'https://www.op.gg/summoners/kr/참새크면비둘기/ingame'): ")
playerLink = "https://www.op.gg/summoners/kr/코코다롱/ingame"
playerName = playerLink.split("/")[-2]
try:
    playerTeam, playerIndex = get_commands(playerLink,playerName)
    print("selected Team:",playerTeam)
    print("selected Index:",playerIndex)
    gameController = ControlGamePlay(playerTeam,playerIndex)
    # print("test1")
    video_file_name = gameController.control()
    # video_file_name = gameController.close_game()
except Exception as e:
    print("Error(Main): %s" % e)