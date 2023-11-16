# -*- coding: utf-8 -*-
import datetime
import shutil
import time
from urllib.parse import unquote
import os
from usecases.get_run_command import get_commands

from usecases.game_controller import ControlGamePlay
import multiprocessing

import time
import pygetwindow as gw
import yt_uploader
from usecases.get_run_command import changePlayedGame

import logging
logging.basicConfig(filename='../LoL stream.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if not os.path.exists("media/AllThumbs"):
    os.makedirs("media/AllThumbs")
if not os.path.exists("media/thumb"):
    os.makedirs("media/thumb")
if not os.path.exists("yt"):
    os.makedirs("yt")

def run_video_uploader(new_folder_path):
    yt_uploader.videoUploader(new_folder_path)


def removeFolder(folder):
    try:
        # Check if the folder exists
        if os.path.exists(folder):
            # Use shutil.rmtree to remove the folder and its contents
            shutil.rmtree(folder)
            print(f"Folder '{folder}' and its contents have been removed.")
            logging.info(f"Main:(removeFolder) Folder '{folder}' and its contents have been removed.")
        else:
            print(f"Folder '{folder}' does not exist.")
            logging.warning(f"Main:(removeFolder) Folder '{folder}' does not exist.")
    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error(f"Main:(removeFolder) Error: {str(e)}")

def closeGame():
    target_window_title = "league of legends (TM) client"

    # Get a list of all open windows
    open_windows = gw.getWindowsWithTitle(target_window_title)

    if open_windows:
        while True:
            print(f"{target_window_title} is open.")
            logging.info(f"Main:(closeGame) {target_window_title} is open.")
            # Close the window

            open_windows = gw.getWindowsWithTitle(target_window_title)
            if open_windows:
                open_windows[0].close()
                print(f"{target_window_title} has been closed.")
                logging.info(f"Main:(closeGame){target_window_title} has been closed.")
                time.sleep(5)
                continue
            else:
                break
    else:
        print(f"{target_window_title} is not open.")
        logging.info(f"Main:(closeGame) {target_window_title} is not open.")


if not os.path.exists("media/gameplay"):
    os.makedirs("media/gameplay")
if not os.path.exists("media/screenshot"):
    os.makedirs("media/screenshot")
if not os.path.exists("../playerLinks.txt"):
    with open("../playerLinks.txt", "w") as player:
        pass

driver = None

recordVideoFolder = r"Z:\Gameplay"


def moveVideo(sourceFolder, destFolder):
    try:
        # Check if the source folder exists
        if not os.path.exists(sourceFolder):
            print(f"Source folder '{sourceFolder}' does not exist.")
            return

        # Check if the destination folder exists, and if not, create it
        if not os.path.exists(destFolder):
            os.makedirs(destFolder)

        # Get a list of all files in the source folder
        files_to_move = os.listdir(sourceFolder)

        # Move each file to the destination folder
        for file in files_to_move:
            source_path = os.path.join(sourceFolder, file)
            dest_path = os.path.join(destFolder, file)
            shutil.move(source_path, dest_path)
            print(f"Moved '{file}' to '{destFolder}'")
            # os.remove(source_path)

    except Exception as e:
        print(f"Error: {str(e)}")


def Run(playerLink):
    global driver
    playerLink = unquote(playerLink, encoding='utf-8')
    # playerLink = "https://www.op.gg/summoners/kr/쪼잔하게 굴지마/ingame"
    playerName = playerLink.split("/")[-2]
    print(f"====> {playerName} <====")
    logging.info(f"Main(Run) ====> {playerName} <====")
    playerTeam = None
    playerIndex = None
    no_of_played_game = None

    base_directory = os.path.abspath('yt')
    current_datetime = datetime.datetime.now()
    folder_name = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    new_folder_path = os.path.join(base_directory, folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    playerTeam, playerIndex, driver, no_of_played_game = get_commands(
        playerLink, playerName, new_folder_path, driver, playerTeam, playerIndex, no_of_played_game)
    # playerTeam, playerIndex, driver, no_of_played_game = "Red",1,driver, 3
    if playerTeam != "None" and playerTeam != "Not found":
        time.sleep(1*90)

        gameController = ControlGamePlay(playerTeam, playerIndex)
        out = gameController.control()

        if out == "crashed":
            removeFolder(new_folder_path)
            changePlayedGame()
        else:
            uploader_process = multiprocessing.Process(target=run_video_uploader, args=(new_folder_path,))
            uploader_process.start()
            
    elif playerTeam == "Not found":
        removeFolder(new_folder_path)
    else:
        removeFolder(new_folder_path)
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
            logging.error("Main(__name__) Error:", str(e))
