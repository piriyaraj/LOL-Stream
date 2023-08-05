# import package
import os
import time
from entities.data_scrapper import DataScrapper as scrapper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# get the player name and get the live player name
driver = ""
gamePath = ""
if gamePath:
    print("Using game play path")


def scrape_lolpros_player(playerLink,playrName):
    playerTeam = ""
    playerIndex = ""
    player_url = f"{playerLink}"
    # print(player_url)
    
    try:       
        driver.get(player_url)
        while True:
            try:
                is_gameplay_found = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='content-container']/div/div/div[2]/div/button[2]")))
                

                print("Found gameplay")
                break
            except:
                print("Gameplay not found")
                driver.refresh()
                time.sleep(5)
        
        # get blue team
        while True:
            team_blue = driver.find_elements(By.XPATH, "//*[@id='content-container']/div/table[1]/tbody/tr/td[4]/a")
            if not team_blue[0].text == "":
                break
            time.sleep(10)
            
        team_red = driver.find_elements(By.XPATH, "//*[@id='content-container']/div/table[2]/tbody/tr/td[4]/a")
        for i in range(len(team_red)):
            player_name = team_red[i].text
            if playrName.lower() in player_name.lower():
                playerTeam = "Red"
                playerIndex = int(i)
                is_gameplay_found.click()
                time.sleep(10)
                return playerTeam, playerIndex
        
        # get red team
        
        for i in range(len(team_blue)):
            player_name = team_blue[i].text
            if playrName.lower() in player_name.lower():
                playerTeam = "Blue"
                playerIndex = int(i)
                is_gameplay_found.click()
                time.sleep(10)
                return playerTeam, playerIndex
    except Exception as e:
        print(f"Error(scrape_lolpros_player): {e}")
        return "None","None"
    # finally:
    #     driver.quit()
def removeGameplay():
    for i in os.listdir(os.path.abspath("media/gameplay")):
        os.remove(os.path.join(os.path.abspath("media/gameplay"),i))
def get_commands(playerLink,playrName):
    removeGameplay()
    
    global driver
    driver = scrapper().driver

    playerTeam, playerIndex = scrape_lolpros_player(playerLink,playrName)
    
    # if playerTeam:
    #     print("Player Team:",playerTeam)
    #     print("Player Index:",playerIndex)
    # else:
    #     print("Scraping failed.")

    driver.quit()

    return playerTeam, playerIndex
