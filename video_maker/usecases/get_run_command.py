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


def scrape_lolpros_player(playerLink,playrName):
    playerTeam = ""
    playerIndex = ""
    player_url = f"{playerLink}"
    print(player_url)
    try:        
        driver.get(player_url)
        adsTag = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div[6]")))
        # live_tab.click()
        
        while True:
            try:
                is_gameplay_found = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='content-container']/div/div/div[2]/div/button[2]")))
                is_gameplay_found.click()

                print("Found gameplay")
                break
            except:
                print("Gameplay not found")
                driver.refresh()
                time.sleep(5)
        
        # get blue team
        team_red = driver.find_elements(By.XPATH, "//*[@id='content-container']/div/table[2]/tbody/tr/td[4]/a")
        for i in range(len(team_red)):
            player_name = team_red[i].text
            print(player_name)
            if playrName.lower() in player_name.lower():
                playerTeam = "Red"
                playerIndex = int(i)
                return playerTeam, playerIndex
        
        # get red team
        team_blue = driver.find_elements(By.XPATH, "//*[@id='content-container']/div/table[1]/tbody/tr/td[4]/a")
        for i in range(len(team_blue)):
            player_name = team_blue[i].text
            print(player_name)
            if playrName.lower() in player_name.lower():
                playerTeam = "Blue"
                playerIndex = int(i)
                return playerTeam, playerIndex
    except Exception as e:
        print(f"Error(scrape_lolpros_player): {e}")
        return "None","None"
    # finally:
    #     driver.quit()
        
def get_commands(playerLink,playrName):
    global driver
    driver = scrapper().driver
    

    playerTeam, playerIndex = scrape_lolpros_player(playerLink,playrName)
    
    if playerTeam:
        print("Player Team:",playerTeam)
        print("Player Index:",playerIndex)
    # else:
    #     print("Scraping failed.")

    driver.quit()

    return playerTeam, playerIndex
