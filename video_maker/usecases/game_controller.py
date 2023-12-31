import os
from time import sleep
import subprocess
import time
import pyautogui
import pydirectinput
from PIL import ImageGrab
from PIL import Image

from usecases.freezefinder import checkFrozen
import time
import pygetwindow as gw


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


class ControlGamePlay:
    def __init__(self, playerTeam, playerIndex) -> None:
        self.__replay_file_dir = os.path.abspath(r'.\media\gameplay')
        self.__player_team = playerTeam
        self.__player_index = str(playerIndex)

    def control(self):
        print("   -start run game")
        status = self.__run_game()
        if status == False:
            return

        status = self.__start_game()
        if status == False:
            closeGame()
            return "crashed"

        time.sleep(5)
        print("   -click center of the screen")
        # Get the size of the screen
        screen_width, screen_height = pydirectinput.size()

        # Calculate the center of the screen
        center_x = int(screen_width / 2)
        center_y = int(screen_height / 2)

        # Click on the center of the screen
        pydirectinput.click(center_x, center_y)
        pydirectinput.keyDown('n')
        pydirectinput.keyUp('n')
        sleep(1)

        # scoreboard
        pydirectinput.keyDown('o')
        pydirectinput.keyUp('o')
        sleep(1)
        # print_progress(51, self.total, prefix='Gameplay recording:')
        pydirectinput.keyDown('u')
        pydirectinput.keyUp('u')
        sleep(2)
        # print_progress(56, self.total, prefix='Gameplay recording:')
        # select champion
        print("   -Selecting player")
        self.__select_player()

        sleep(2)
        # Extend character stats
        pydirectinput.keyDown('c')
        pydirectinput.keyUp('c')
        sleep(1)
        # print_progress(59, self.total, prefix='Gameplay recording:')
        # zoom out
        print("   -Zoom out the screen!")
        # Click on the center of the screen
        pydirectinput.click(center_x, center_y)
        # Press and hold Ctrl+Shift+Z
        pydirectinput.keyDown('ctrl')
        pydirectinput.keyDown('shift')
        pydirectinput.keyDown('z')
        pydirectinput.keyUp('ctrl')
        pydirectinput.keyUp('shift')
        pydirectinput.keyUp('z')
        # Move mouse pointer down 5 times
        pyautogui.scroll(-700)

        self.close_game()
        # sleep(60*3)
        return True

    def __start_game(self):
        print('  -Wait for start game')
    # Load the target image
        target_image = Image.open(
            os.path.abspath("assets/img/startButton.png"))
        count = 0
        while True:
            screenshot = ImageGrab.grab()  # Take a screenshot of the entire screen
            # Find the target image on the screenshot
            result = pyautogui.locateOnScreen(target_image, confidence=0.64)

            if result is not None:
                # Get the center of the found image
                button_position = pyautogui.center(result)
                print("  -game starting !")
                return True  # Return True after clicking
            else:
                time.sleep(10)  # Wait for a second before checking again
                if count >= 4*60:
                    return False
                count += 10

    def close_game(self):
        print('  -Wait for closing game')
        # Load the target image
        # status = checkFrozen()
        # sleep(3)
        # pyautogui.hotkey('alt', 'f4')
        # sleep(10)
        # print("  -Close button clicked!")
        # return
        target_image = Image.open(
            os.path.abspath("assets/img/closeButton.png"))
        while True:
            # screenshot = ImageGrab.grab()  # Take a screenshot of the entire screen
            # screenshot.save("media/screenshot/screenshot.jpg")
            # Find the target image on the screenshot
            result = pyautogui.locateOnScreen(target_image, confidence=0.8)
            # result1 = pyautogui.locateOnScreen(target_image1, confidence=0.95)
            if result is not None:
                sleep(3)
                pyautogui.hotkey('alt', 'f4')
                sleep(1)

                print("  -Close button clicked!")
                return True  # Return True after clicking
            else:
                time.sleep(10)  # Wait for a second before checking again

    def __run_game(self):
        try:
            file = os.listdir(self.__replay_file_dir)[0]
            subprocess.run(
                ["start", "cmd", "/c", f"{self.__replay_file_dir}\{file}"], shell=True)
            return True
        except:
            return False

    def __select_player(self):
        if self.__player_team == 'Blue':
            # f1
            pydirectinput.keyDown('f3')
            pydirectinput.keyUp('f3')
            pydirectinput.keyDown(self.__player_index)
            pydirectinput.keyUp(self.__player_index)
            pydirectinput.keyDown(self.__player_index)
            pydirectinput.keyUp(self.__player_index)
        else:
            keys = ['q', 'w', 'e', 'r', 't']
            # f2
            pydirectinput.keyDown('f3')
            pydirectinput.keyUp('f3')
            pydirectinput.keyDown(
                keys[int(self.__player_index) - 1])
            pydirectinput.keyUp(
                keys[int(self.__player_index) - 1])
            pydirectinput.keyDown(
                keys[int(self.__player_index) - 1])
            pydirectinput.keyUp(
                keys[int(self.__player_index) - 1])
