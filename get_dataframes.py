import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import requests

from selenium.webdriver import Chrome
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import json

url = "https://www.leagueofgraphs.com/summoner/tr/caydanlik31-aldrc"
driver = Chrome()
driver.maximize_window()

t = time.time()
driver.set_page_load_timeout(10)

try:
    driver.get(url)
except TimeoutException:
    driver.execute_script("window.stop();")

####### GENERAL INFO (RANKS ETC)

current_rank = driver.find_elements(By.XPATH,
                                   '//*[@id="mainContent"]/div[1]/div[1]/div[1]/div[1]/div/div[1]/div/div/div[2]')
# rank info
rank_info_list = []
for rank_info in current_rank:
    rank_info_list.append(rank_info.text)

# previous ranks

prev_rank_list = []
for idx in range(6):
    prev_path = '//*[@id="mainContent"]/div[1]/div[1]/div[3]/div[' + str(idx + 1) + ']'
    prev_rank = driver.find_element(By.XPATH, prev_path)
    prev_rank_list.append(prev_rank.text)

# last match table (120 matches)

counter = 12
idx = 13
wait = WebDriverWait(driver,20)
while counter > 0:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, -200);")
    time.sleep(2)
    path = '//*[@id="mainContent"]/div[1]/div[1]/div[5]/table/tbody/tr[' + str(idx) + ']/td/button'
    wait.until(EC.element_to_be_clickable((By.XPATH, path))).click()
    time.sleep(5)
    #button.click()
    #time.sleep(5)
    counter -= 1
    idx += 10

table = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[1]/div[1]/div[5]/table/tbody')


titles = ["game_result", "time", "kda", "vis/cs_score", "kill_p."]
df = pd.DataFrame(columns=titles)

for tr in table.find_elements(By.XPATH, 'tr')[2:122]:

    row = [item.text for item in tr.find_elements(By.XPATH, "td")]
    row = [item for item in row if item]

    # seperate first column
    first_elem = row[0].split('\n')
    row[0] = first_elem[0]
    row.insert(1, first_elem[3])

    # seperate kda column
    if (row[0] != "Remake"):
        second_elem = row[2].split('\n')
        row[2] = second_elem[0]
        row.insert(3, second_elem[1].split(" - ")[0])
        row.insert(4, second_elem[1].split(" - ")[1])
    else:
        continue

    l = len(df)
    df.loc[l] = row[:-1]

# CHAMP DF
driver.execute_script("window.scrollTo(0, document.body.scrollTop);")
time.sleep(2)
champ_button = driver.find_element(By.XPATH, '//*[@id="filters-menu"]/div[2]/div[2]/a')
time.sleep(4)
champ_button.click()

champ_table = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[1]/div/div/div[2]/div[1]/div/table/tbody')
time.sleep(2)
titles = champ_table.find_elements(By.XPATH, "tr")[0]
time.sleep(2)

headers = []
for header in titles.find_elements(By.XPATH, "th"):
    headers.append(header.text)

headers.pop()

df_champ = pd.DataFrame(columns=headers)

for tr in champ_table.find_elements(By.XPATH, "tr")[1:]:
    row = [item.text for item in tr.find_elements(By.XPATH, "td")]
    l = len(df_champ)
    df_champ.loc[l] = row[:-1]

time.sleep(2)

# champion (xerath) performance
# just list them (no graphs or sth.)

champ_button = driver.find_element(By.XPATH, '//*[@id="filters-menu"]/div[2]/div[2]/a')
time.sleep(20)
champ_button.click()
time.sleep(2)

df_champ = pd.read_csv("df_champ.csv")
max_champ = df_champ.loc[df_champ["Played"] == df_champ["Played"].max()]["Champion"].squeeze()

xerath_button = driver.find_element(By.XPATH,
                                    '//*[@id="mainContent"]/div[1]/div/div/div[2]/div[1]/div/table/tbody/tr[2]/td[1]/a')
time.sleep(2)
xerath_button.click()

pie_chart = driver.find_elements(By.CLASS_NAME, "pie-chart-container")

chart_1 = []
chart_2 = []
for chart in pie_chart:
    chart_name = chart.find_elements(By.CLASS_NAME, "pie-chart-title")
    time.sleep(2)
    chart_value = chart.find_elements(By.CLASS_NAME, "pie-chart")
    chart_1.append(chart_name[0].text)
    chart_2.append(chart_value[0].text)

charts = zip(chart_1, chart_2)

charts = [*charts]

charts.append(rank_info_list)
charts.append(prev_rank_list)

json_data = json.dumps(charts, indent=2)

with open("charts", "w") as json_file:
    json_file.write(json_data)

#df.to_csv("df.csv", index=False)
#df_champ.to_csv("df_champ.csv", index=False)