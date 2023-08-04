# import package
import os
import time
from entities.data_scrapper import DataScrapper as scrapper
from entities.logger import logging as logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# get the player name and get the live player name
driver = ""
gamePath = ""
if gamePath:
    print("Using game play path")
 
def build_runner(command):
    cmds = command.split("&")
    batch_script_path = os.path.abspath("media/gameplay/Runner.cmd")
    
    
    with open(batch_script_path, 'w') as file:
        for cmd in cmds:
            file.write(cmd.strip() + "\n")  

def scrape_lolpros_player(ChampionName):
    playerTeam = ""
    playerIndex = ""
    player_url = f"https://www.op.gg/summoners/euw/{ChampionName}/ingame"
    print(player_url)
    try:        
        driver.get(player_url)
        adsTag = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div[6]")))
        # live_tab.click()
        while True:
            try:
                is_gameplay_found = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='content-container']/div/div/div[2]/div/button[2]")))
                break
            except:
                print("Gameplay not found")
                driver.refresh()
                time.sleep(5)
        
        # get blue team
        team_red = driver.find_elements(By.XPATH, "//*[@id='content-container']/div/table[2]/tbody/tr/td[4]/a")
        for i in range(len(team_red)):
            player_name = team_red[i].text
            if ChampionName.lower() in player_name.lower():
                return playerTeam, playerIndex
        
        # get red team
        team_blue = driver.find_elements(By.XPATH, "//*[@id='current-game']/div[1]/div/div[3]/div/div[2]/div/div[1]")
        for i in range(len(team_blue)):
            player_name = team_blue[i].text
            if ChampionName.lower() in player_name.lower():
                return playerTeam, playerIndex
    except Exception as e:
        print(f"Error(scrape_lolpros_player): {e}")
        return "None","None"
    # finally:
    #     driver.quit()

# get the LOL run command
def get_command(playerName):
    servers =['BR', 'EUNE', 'EUW', 'JP', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'RU', 'TR', 'PH', 'SG', 'TH', 'TW', 'VN']
    for server in servers:
        try:
            player_url = f"https://lolspectator.tv/spectate?name={playerName}&region={server}"
            driver.get(player_url)
            live_tab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='windows-script']")))
            cmd = live_tab.text
            return cmd
        except Exception as e:
            print(f"Error: {e}")

        
def get_commands(ChampionName):
    global driver
    driver = scrapper().driver
    

    playerTeam, playerIndex = scrape_lolpros_player(ChampionName)
    
    if playerTeam:
        print("Player Name:",playerTeam)
    else:
        print("Scraping failed.")

    driver.quit()

    return playerTeam, playerIndex
