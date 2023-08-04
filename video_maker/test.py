import os
import subprocess
from usecases.get_run_command import get_commands
import subprocess

from usecases.record_video import ControlGamePlay

if not os.path.exists("media/gameplay"):
    os.makedirs("media/gameplay")
    
def run_in_new_terminal(command):
    cmds = command.split("&")
    batch_script_path = os.path.abspath("media/gameplay/Runner.cmd")
    
    with open(batch_script_path, 'w') as file:
        for cmd in cmds:
            file.write(cmd.strip() + "\n")
    # subprocess.Popen(['start', 'cmd', '/c', batch_script_path], shell=True)

playerLink = "https://www.op.gg/summoners/kr/viper3/ingame"
playrName = "viper3"

try:
    playerTeam, playerIndex = get_commands(playerLink,playrName)
   
    print("Player Team:",playerTeam)
    print("Player Index:",playerIndex)
    # command = """ cd /d "C:\Riot Games\League of Legends\Game" & "League of Legends.exe" "spectator spectator-consumer.euw1.lol.pvp.net:80 YQHBRhh4BwsDqaJyYm6ulqnT1NkkKki8 6534915822 EUW1" "-UseRads" """
    # run_in_new_terminal(command)
    # gameController = ControlGamePlay("Blue",1)
    # video_file_name = gameController.record()
    # video_file_name = gameController.select_video_file()
except Exception as e:
    print("Error(test): %s" % e)