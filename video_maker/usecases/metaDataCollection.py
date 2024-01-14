from datetime import datetime
import json
from entities.match_data import MatchData, Player
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import os
from selenium.webdriver.common.by import By

import time

from usecases.data import save
match_data: MatchData = {
    "team1": {
        "players": []
    },
    "team2": {
        "players": []
    }
}
playerName = None


def __create_player(name: str, kda: str, rank: str, champion: str, spell=[]) -> Player:
    # print("=========>:",name)
    # if len(name.split("#")>1):
    name = name.split("#")
    if len(name)>=1:
        name = name[0]
    return {
        "name": name,
        "kda": kda,
        "rank": rank,
        "champion": champion,
        "spell": spell
    }


def __create_team_red(driver) -> list[Player]:
    team_one = []
    # print("====team x======")
    team_red_names = driver.find_elements(
        By.XPATH, "//*[@id='content-container']/div/table[2]/tbody/tr/td[4]/a")
    redPlayerNames = []

    for i in range(len(team_red_names)):
        player_name = team_red_names[i].text.split("#")[0]
        redPlayerNames.append(player_name)
    # print(redPlayerNames)

    redPlayerKDA = []
    team_red_kda = driver.find_elements(
        By.XPATH, "//*[@id='content-container']/div/table[2]/tbody/tr/td[9]")
    for i in range(len(team_red_kda)):
        try:
            player_kda = team_red_kda[i].text.split(
                " KDA\n")[1].replace(" ", "")
        except:
            player_kda = "-/-/-"
        redPlayerKDA.append(player_kda)

    # print("  ===== cp1")
    redPlayerRank = []
    team_red_rank = driver.find_elements(
        By.XPATH, "//*[@id='content-container']/div/table[2]/tbody/tr/td[5]")
    for i in range(len(team_red_rank)):
        try:
            player_rank = team_red_rank[i].find("//img").get_attribute("alt")
        except:
            player_rank = "Iron"
        redPlayerRank.append(player_rank)
    # print("  ===== cp2")

    redPlayerChampion = []
    team_red_champion = driver.find_elements(
        By.XPATH, "//*[@id='content-container']/div/table[2]/tbody/tr/td[1]//img")
    for i in range(len(team_red_champion)):
        player_champion = team_red_champion[i].get_attribute("alt")
        redPlayerChampion.append(player_champion)
    # print("  ===== cp3")

    redPlayerSpell = []
    team_red_spell = driver.find_elements(
        By.XPATH, "//*[@id='content-container']/div/table[2]/tbody/tr/td[2]")
    for i in range(len(team_red_spell)):
        li = []
        li.append(driver.find_element(
            By.XPATH, f"//*[@id='content-container']/div/table[2]/tbody/tr[{i+1}]/td[2]/div[1]//img").get_attribute("alt"))
        li.append(driver.find_element(
            By.XPATH, f"//*[@id='content-container']/div/table[2]/tbody/tr[{i+1}]/td[2]/div[2]//img").get_attribute("alt"))
        redPlayerSpell.append(li)

    # print("  ===== cp4")
    # for i in range(len(redPlayerKDA)):
    #     print(redPlayerNames[i],":",redPlayerKDA[i],":",redPlayerChampion[i],":",redPlayerSpell[i])
    team_one.append(__create_player(
        name=redPlayerNames[0], kda=redPlayerKDA[0], rank=redPlayerRank[0], champion=redPlayerChampion[0], spell=redPlayerSpell[0]))
    # print("  ===== cp5")

    team_one.append(__create_player(
        name=redPlayerNames[1], kda=redPlayerKDA[1], rank=redPlayerRank[1], champion=redPlayerChampion[1], spell=redPlayerSpell[1]))
    team_one.append(__create_player(
        name=redPlayerNames[2], kda=redPlayerKDA[2], rank=redPlayerRank[2], champion=redPlayerChampion[2], spell=redPlayerSpell[2]))
    team_one.append(__create_player(
        name=redPlayerNames[3], kda=redPlayerKDA[3], rank=redPlayerRank[3], champion=redPlayerChampion[3], spell=redPlayerSpell[3]))
    team_one.append(__create_player(
        name=redPlayerNames[4], kda=redPlayerKDA[4], rank=redPlayerRank[4], champion=redPlayerChampion[4], spell=redPlayerSpell[4]))
    # print("  ===== cp6")

    return team_one


def __create_team_blue(driver) -> list[Player]:
    team_one = []
    # print("====team x======")
    team_red_names = driver.find_elements(
        By.XPATH, "//*[@id='content-container']/div/table[1]/tbody/tr/td[4]/a")
    redPlayerNames = []
    redPlayerKDA = []
    for i in range(len(team_red_names)):
        player_name = team_red_names[i].text.split("#")[0]
        redPlayerNames.append(player_name)
    # print(redPlayerNames)
    redPlayerKDA = []
    team_red_kda = driver.find_elements(
        By.XPATH, "//*[@id='content-container']/div/table[1]/tbody/tr/td[9]")
    for i in range(len(team_red_kda)):
        try:
            player_kda = team_red_kda[i].text.split(
                " KDA\n")[1].replace(" ", "")
        except:
            player_kda = "-/-/-"
        redPlayerKDA.append(player_kda)

    redPlayerRank = []
    team_red_rank = driver.find_elements(
        By.XPATH, "//*[@id='content-container']/div/table[1]/tbody/tr/td[5]")
    for i in range(len(team_red_rank)):
        try:
            player_rank = team_red_rank[i].find("//img").get_attribute("alt")
        except:
            player_rank = "Iron"
        redPlayerRank.append(player_rank)
    # print(redPlayerRank)
    redPlayerChampion = []
    team_red_champion = driver.find_elements(
        By.XPATH, "//*[@id='content-container']/div/table[1]/tbody/tr/td[1]//img")
    for i in range(len(team_red_champion)):
        player_champion = team_red_champion[i].get_attribute("alt")
        redPlayerChampion.append(player_champion)

    redPlayerSpell = []
    team_red_spell = driver.find_elements(
        By.XPATH, "//*[@id='content-container']/div/table[1]/tbody/tr/td[2]")
    for i in range(len(team_red_spell)):
        li = []
        li.append(driver.find_element(
            By.XPATH, f"//*[@id='content-container']/div/table[1]/tbody/tr[{i+1}]/td[2]/div[1]//img").get_attribute("alt"))
        li.append(driver.find_element(
            By.XPATH, f"//*[@id='content-container']/div/table[1]/tbody/tr[{i+1}]/td[2]/div[2]//img").get_attribute("alt"))
        redPlayerSpell.append(li)
    # print("      cp2        ==============")
    # print(len(redPlayerNames),":",len(redPlayerKDA),":",len(redPlayerRank),":",len(redPlayerChampion),":",len(redPlayerSpell))

    # for i in range(len(redPlayerNames)):
    #     print(redPlayerNames[i],":",redPlayerKDA[i],":",redPlayerRank[i],":",redPlayerChampion[i],":",redPlayerSpell[i])
    team_one.append(__create_player(
        name=redPlayerNames[0], kda=redPlayerKDA[0], rank=redPlayerRank[0], champion=redPlayerChampion[0], spell=redPlayerSpell[0]))
    team_one.append(__create_player(
        name=redPlayerNames[1], kda=redPlayerKDA[1], rank=redPlayerRank[1], champion=redPlayerChampion[1], spell=redPlayerSpell[1]))
    team_one.append(__create_player(
        name=redPlayerNames[2], kda=redPlayerKDA[2], rank=redPlayerRank[2], champion=redPlayerChampion[2], spell=redPlayerSpell[2]))
    team_one.append(__create_player(
        name=redPlayerNames[3], kda=redPlayerKDA[3], rank=redPlayerRank[3], champion=redPlayerChampion[3], spell=redPlayerSpell[3]))
    team_one.append(__create_player(
        name=redPlayerNames[4], kda=redPlayerKDA[4], rank=redPlayerRank[4], champion=redPlayerChampion[4], spell=redPlayerSpell[4]))
    # print("        cp4            =====")
    return team_one


def getMetaData(driver, playerUrl, folder):
    playerName = playerUrl.split("/")[-2].split('-')
    if len(playerName) >= 1:
        playerName = playerName[0]

    # print("==================>",playerName)
    match_data['region'] = playerUrl.split("/")[-3]
    match_data['team1']['result'] = "Blue"
    match_data['team2']['result'] = "Red"
    patch = driver.find_element(
        by=By.XPATH, value='//nav[@class="route-nav"]//span[2]').text
    match_data['patch'] = patch
    # print("   =================> cp1")
    # match_data['patch'] = '13.22'
    data = __create_team_blue(driver)
    print("   > Got blue team data")
    match_data['team1']['players'] = data
    # print("Got blue team")
    match_data['team2']['players'] = __create_team_red(driver)
    print("   > Got blue team")
    # mvp_data = __get_mvp_data(match_data)
    # match_data['mvp'] = match_data[mvp_data['team']]['players'][mvp_data['player_index']]
    # match_data['loser'] = match_data[mvp_data['loser_team']
    #                                             ]['players'][mvp_data['player_index']]['champion']
    # match_data['player_role'] = mvp_data['player_role']
    # match_data['player_index'] = str(int(mvp_data['player_index']) + 1)

    team_red = driver.find_elements(
        By.XPATH, "//*[@id='content-container']/div/table[2]/tbody/tr/td[4]/a")
    isFound = False
    playerTeam = 'team1'
    playerIndex = 0
    # print("===> Red")

    for i in range(len(team_red)):
        player_name = team_red[i].text

        # print(playerName.lower(),player_name.lower().strip())
        if playerName.lower() in player_name.lower().strip():
            playerTeam = "Red"
            playerTeam = "team2"
            playerIndex = int(i)
            # press_update_button(driver)
            isFound = True
            # time.sleep(10)

    # get blue team
    # print("===> Blue")
    team_blue = driver.find_elements(
        By.XPATH, "//*[@id='content-container']/div/table[1]/tbody/tr/td[4]/a")
    if not isFound:
        for i in range(len(team_blue)):
            player_name = team_blue[i].text
            # print(playerName.lower(),player_name.lower().strip())

            if playerName.lower() in player_name.lower().strip():
                playerTeam = "Blue"
                playerTeam = "team1"
                playerIndex = int(i)

    # print("  -selected Team:", playerTeam)
    # print("  -selected Index:", playerIndex+1)
    loserTeam = "team1"
    if playerTeam == "team1":
        loserTeam = "team2"
    match_data['mvp'] = match_data[playerTeam]['players'][playerIndex]
    match_data['loser'] = match_data[loserTeam]['players'][playerIndex]['champion']
    match_data['date'] = str(datetime.now().strftime("%d/%m/%Y"))
    save(match_data, folder)
    return match_data


def __get_mvp_data(match_data):
    team = ''
    kdas = []
    if match_data['team1']['result'] == 'Victory':
        for player in match_data['team1']['players']:
            team = 'team1'
            loser_team = 'team2'
            values = player['kda'].split(" / ")
            if values[1] == '0':
                values[1] = 1
            kdaValue = (int(values[0])+int(values[2]))/int(values[1])
            kdas.append(kdaValue)
    else:
        for player in match_data['team2']['players']:
            team = 'team2'
            loser_team = 'team1'
            values = player['kda'].split(" / ")
            if values[1] == '0':
                values[1] = 1
            kdaValue = (int(values[0])+int(values[2]))/int(values[1])
            kdas.append(kdaValue)
    player_index = kdas.index(max(kdas))
    roles = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']
    return {
        "team": team,
        "player_index": player_index,
        "loser_team": loser_team,
        "player_role": roles[player_index]
    }


if __name__ == '__main__':
    driver = webdriver.Firefox()
    playerUrl = "https://www.op.gg/summoners/kr/cheon2/ingame"
    driver.get(playerUrl)
    playerName = playerUrl.split("/")[-2]
    match_data['region'] = playerUrl.split("/")[-3]
    while True:
        try:
            team_blue = driver.find_elements(
                By.XPATH, "//*[@id='content-container']/div/table[1]/tbody/tr/td[4]/a")
            if not team_blue[0].text == "":
                break
        except Exception as e:
            print(e)
            time.sleep(2)
    print("Started")
    getMetaData(driver)
