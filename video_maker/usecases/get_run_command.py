# import package
import time
from entities.data_scrapper import DataScrapper as scrapper
from entities.logger import logging as logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# get the player name and get the live player name
driver = scrapper().driver

def scrape_lolpros_player(player_url):
    try:        
        driver.get(player_url)
        live_tab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']/main/div/div/div[2]/div/ul/li[2]/a")))
        live_tab.click()
        while True:
            try:
                is_gameplay_found = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='current-game']/div[1]/div/div[1]")))
                break
            except:
                print("Gameplay not found")
                refreshButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='current-game']/div/button")))
                refreshButton.click()
                time.sleep(1)
        
        # get blue team
        team_red = driver.find_elements(By.XPATH, "//*[@id='current-game']/div[1]/div/div[2]/div/div[2]/div/div[1]")
        player_name_tags = driver.find_elements(By.XPATH, "//*[@id='current-game']/div[1]/div/div[2]/div/div[2]/div/div[2]")
        for i in range(len(team_red)):
            player_name = team_red[i].text
            if "wenbo" in player_name.lower():
                return player_name_tags[i].text
        
        # get red team
        team_blue = driver.find_elements(By.XPATH, "//*[@id='current-game']/div[1]/div/div[3]/div/div[2]/div/div[1]")
        player_name_tags = driver.find_elements(By.XPATH, "//*[@id='current-game']/div[1]/div/div[3]/div/div[2]/div/div[2]")
        for i in range(len(team_blue)):
            player_name = team_blue[i].text
            if "wenbo" in player_name.lower():
                return player_name_tags[i].text
    except Exception as e:
        print(f"Error: {e}")
        return None
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
    player_url = f"https://lolpros.gg/player/{ChampionName}"
    print(player_url)
    logger.info("Monitoring player: {}".format(player_url))

    playerName = scrape_lolpros_player(player_url)
    
    if playerName:
        print("Player Name:",playerName)
    else:
        print("Scraping failed.")
        return

    command = get_command(playerName)
    print("command:",command)
    driver.quit()
    return command
