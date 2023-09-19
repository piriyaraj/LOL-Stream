# import package
import os
import time
from entities.data_scrapper import DataScrapper as scrapper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import pydirectinput

# get the player name and get the live player name
playedGames = []
is_cookie_button_pressed = False


def is_game_already_played():
    file = os.listdir(os.path.abspath(r'.\media\gameplay'))[0]
    print("  -gamePlay: " + file)
    
    
    with open(os.path.join(os.path.abspath(r'.\media\gameplay'), file), 'r') as runnerfile:
        data = runnerfile.read()
    # print("check 0")
    gameId = data.split(".lol.pvp.net:80 ")[1].split('" "-UseRads')[0]
    # print("check 0.1",playedGames)
    if gameId in playedGames:
        return True
    else:
        playedGames.append(gameId)
        return False


def get_no_played_game(team, index, driver):
    if team == "Blue":
        team_index = 1
    else:
        team_index = 2
    # //*[@id="content-container"]/div/table[1]/tbody/tr[5]/td[8]
    xpath = f"//*[@id='content-container']/div/table[{team_index}]/tbody/tr[{index}]/td[8]"
    rand_text = driver.find_element(By.XPATH, xpath)
    while True:
        rand_text = driver.find_element(By.XPATH, xpath)
        if not rand_text.text == "":
            break
    rank = rand_text.text.split("(")[1].split()[0]
    print("  -Played: " + rank)
    return rank


def press_update_button(driver):
    xpath = "//button[@class='css-1ki6o6m e18vylim0']"
    try:
        updateButton = driver.find_element(By.XPATH, xpath)
        updateButton.click()
        print("  -Update button clicked")
        time.sleep(1)
        try:
            alert = Alert(driver)
            alert.accept()
        except:
            pass

    except Exception as e:
        # print("  -Error(press_update_button): " + str(e))
        print("  -Update button not found")


def scrape_lolpros_player(playerLink, playrName, driver, team, index, no_of_played_game):
    global is_cookie_button_pressed
    playerTeam = ""
    playerIndex = ""
    player_url = f"{playerLink}"
    # print(player_url)
    updated_no_played_game = None
    try:
        driver.get(player_url)
        while True:
            try:
                is_gameplay_found = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "//button[@class='spectate css-1wruk4q eh5kfb0' and @type='button']")))
                # time.sleep(5)
                if not is_cookie_button_pressed:
                    try:
                        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, "//button[@mode='primary' and @size='large' and contains(span, 'GODKÄNN')]")))
                        button.click()
                        time.sleep(1)
                        print("  -cookies button pressed")
                        is_cookie_button_pressed = True
                    except Exception as e:
                        pass
                if team is not None:
                    updated_no_played_game = get_no_played_game(
                        team, index, driver)
                    if no_of_played_game == updated_no_played_game:
                        print("Already played game Found")
                        # press_update_button(driver)
                        time.sleep(5)
                        driver.get(player_url)
                        time.sleep(5)
                        continue
                print("New live game found")

                removeGameplay()
                break
            except Exception as e:
                print("Live game not found")
                # press_update_button(driver)
                time.sleep(1)
                return "None", 0, driver, "None"
                break
                driver.get(player_url)
                time.sleep(5)

        # get blue team
        while True:
            team_blue = driver.find_elements(
                By.XPATH, "//*[@id='content-container']/div/table[1]/tbody/tr/td[4]/a")
            if not team_blue[0].text == "":
                break
            time.sleep(2)

        isFound = False
        team_red = driver.find_elements(
            By.XPATH, "//*[@id='content-container']/div/table[2]/tbody/tr/td[4]/a")
        for i in range(len(team_red)):
            player_name = team_red[i].text
            if playrName.lower() in player_name.lower():
                playerTeam = "Red"
                playerIndex = int(i)
                # press_update_button(driver)
                isFound = True
                # time.sleep(10)

        # get red team
        if not isFound:
            for i in range(len(team_blue)):
                player_name = team_blue[i].text
                if playrName.lower() in player_name.lower():
                    playerTeam = "Blue"
                    playerIndex = int(i)
                    # press_update_button(driver)
                    # time.sleep(10)

        print("  -selected Team:", playerTeam)
        print("  -selected Index:", playerIndex+1)
        # if team is None :
        #     index = int(playerIndex)+1
        #     team = playerTeam
        #     updated_no_played_game = get_no_played_game(team,index,driver)

        is_gameplay_found.click()
        time.sleep(10)
        # click close button
        status = is_game_already_played()
        # print("check 1")
        if status:
            print("  -already_played")
            return "None", 0, driver, "None"
        try:
            button = driver.find_element(By.XPATH, "//button[@class='close']")
            button.click()
            time.sleep(2)
        except Exception as e:
            print("Error(click download):", e)
        # press_update_button(driver)
        return playerTeam, playerIndex, driver, updated_no_played_game

    except Exception as e:
        print(f"Error(scrape_lolpros_player): {e}")
        return "None", 0, driver, "None"
    # finally:
    #     driver.quit()


def removeGameplay():
    for i in os.listdir(os.path.abspath("media/gameplay")):
        os.remove(os.path.join(os.path.abspath("media/gameplay"), i))


def get_commands(playerLink, playrName, driver=None, team=None, index=None, no_of_played_game=None):
    if driver is None:
        driver = scrapper().driver

    playerTeam, playerIndex, driver, no_of_played_game = scrape_lolpros_player(
        playerLink, playrName, driver, team, index, no_of_played_game)

    return playerTeam, int(playerIndex)+1, driver, no_of_played_game
