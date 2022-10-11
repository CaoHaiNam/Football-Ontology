import os
import re
import time
import random
import json
from glob import glob
from pathlib import Path
import traceback
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManagerclear
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import TimeoutException
from selenium.webdriver import DesiredCapabilities
# from googletranslate import translate

chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--incognito')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
chrome_options.add_argument(f'--user-agent={user_agent}')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_experimental_option('w3c', False)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--window-size=1920x1080')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--allow-running-insecure-content')

capabilities = DesiredCapabilities.CHROME.copy()
capabilities['browserName'] = 'chrome'
capabilities['chromeOptions'] = {'args': ['no-sandbox']}
capabilities['acceptSslCerts'] = True
capabilities['acceptInsecureCerts'] = True
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
path_chrome_driver = os.path.abspath("chromedriver")


class AutoGenerator(object):
    def __init__(self):
        self.data = dict()
        self.resp_list = list()
        self.driver = webdriver.Chrome(path_chrome_driver, options=chrome_options, desired_capabilities=capabilities)


    def get_team_id(self):
        try:
            self.driver.get('https://1xbet.whoscored.com/Regions/252/Tournaments/2/Seasons/9075/Stages/20934/Show/England-Premier-League')
            time.sleep(random.randint(1, 5))

            tables = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#standings-20934-content')))
            trs = tables.find_elements(By.CSS_SELECTOR, 'tr')
            ls = [{"team_id": i.get_attribute("data-team-id"), "name": i.find_element(By.CSS_SELECTOR, 'td > a').text} for i in trs]
            if ls:
                data = ls
            else:
                data = []

            # print(data)
            with open(f'data/team_id.json', 'w', encoding='utf8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            self.driver.quit()

            return data

        except TimeoutException:
            print(f'error timeout or over 10000 characters')
            self.data["message"] = 401
            self.data["results"] = "Error timeout or over 10000 characters"
            self.driver.quit()

        except NoSuchElementException:
            print(f'No element were found matching your selection')
            self.driver.quit()

        except ElementClickInterceptedException:
            print(f"Can't click to element your selection")
            self.driver.quit()


    def get_team_info(self, teamIds=None):
        try:
            # teamIds = 14
            self.driver.get(f'https://1xbet.whoscored.com/StatisticsFeed/1/GetPlayerStatistics?category=summary&subcategory=all&statsAccumulationType=0&isCurrent=true&playerId=&teamIds={teamIds}&matchId=&stageId=&tournamentOptions=2&sortBy=Rating&sortAscending=&age=&ageComparisonType=&appearances=&appearancesComparisonType=&field=Overall&nationality=&positionOptions=&timeOfTheGameEnd=&timeOfTheGameStart=&isMinApp=false&page=&includeZeroValues=true&numberOfPlayersToPick=')
            content = self.driver.find_element(By.TAG_NAME, 'body').text

            content = json.loads(content)
            # print(content)

            # with open(f'data/all_footballers_team_{teamIds}.json', 'w', encoding='utf8') as f:
            #     json.dump(content, f, ensure_ascii=False, indent=4)

            return content

        except TimeoutException:
            print(f'error timeout or over 10000 characters')
            self.data["message"] = 401
            self.data["results"] = "Error timeout or over 10000 characters"

        except NoSuchElementException:
            print(f'No element were found matching your selection')

        except ElementClickInterceptedException:
            print(f"Can't click to element your selection")


    def get_player_info(self, playerId=None):
        try:
            # playerId = 279379
            # playerId = 122366
            self.driver.get(f'https://1xbet.whoscored.com/StatisticsFeed/1/GetPlayerStatistics?category=summary&subcategory=all&statsAccumulationType=0&isCurrent=true&playerId={playerId}&teamIds=&matchId=&stageId=&tournamentOptions=&sortBy=Rating&sortAscending=&age=&ageComparisonType=&appearances=&appearancesComparisonType=&field=Overall&nationality=&positionOptions=&timeOfTheGameEnd=&timeOfTheGameStart=&isMinApp=false&page=&includeZeroValues=true&numberOfPlayersToPick=')
            content = self.driver.find_element(By.TAG_NAME, 'body').text

            # print(content)

            content = json.loads(content)

            with open(f'football_player_info_1/{playerId}.json', 'w', encoding='utf8') as f:
                json.dump(content, f, ensure_ascii=False, indent=4)


            return content

        except TimeoutException:
            print(f'error timeout or over 10000 characters')
            self.data["message"] = 401
            self.data["results"] = "Error timeout or over 10000 characters"

        except NoSuchElementException:
            print(f'No element were found matching your selection')

        except ElementClickInterceptedException:
# Getting the playerIds from the team_id.json file and then using the playerIds to get the player
# info.
            print(f"Can't click to element your selection")


if __name__ == '__main__':
    # x = AutoGenerator().get_team_id()
    # print(x)
    with open('data/team_id.json', 'r', encoding='utf8') as f:
        team_id = json.load(f)
    playerIds = []
    for i in team_id:
        team_id = i['team_id']
        team_info = AutoGenerator().get_team_info(team_id)['playerTableStats']
        for j in team_info:
            # print(j[''])
            playerIds.append(j['playerId'])
    # print(playerIds)
    for i in playerIds:
        AutoGenerator().get_player_info(i)


    