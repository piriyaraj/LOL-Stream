import os
import subprocess
from usecases.get_run_command import get_commands
import subprocess

from usecases.game_controller import ControlGamePlay

if not os.path.exists("media/gameplay"):
    os.makedirs("media/gameplay")
    
def run_in_new_terminal(command):
    cmds = command.split("&")
    batch_script_path = os.path.abspath("media/gameplay/Runner.cmd")
    
    with open(batch_script_path, 'w') as file:
        for cmd in cmds:
            file.write(cmd.strip() + "\n")
    # subprocess.Popen(['start', 'cmd', '/c', batch_script_path], shell=True)

playerLink = input("Enter ingame player Link (EX:'https://www.op.gg/summoners/kr/참새크면비둘기/ingame'): ")
# playerLink = "https://www.op.gg/summoners/kr/참새크면비둘기/ingame"
playerName = playerLink.split("/")[-2]
try:
    playerTeam, playerIndex = get_commands(playerLink,playerName)

    gameController = ControlGamePlay(playerTeam,playerIndex)
    video_file_name = gameController.control()
except Exception as e:
    print("Error(test): %s" % e)