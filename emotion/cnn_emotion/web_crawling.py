from bs4 import BeautifulSoup as BS
import requests as req
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


def find(wait, css_selector):
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))


def find_music(emotion):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("headless")

    chrome = webdriver.Chrome(
        'cnn_emotion/chromedriver.exe', options=options)

    url = 'https://www.melon.com/dj/themegenre/djthemegenre_list.htm'
    chrome.get(url)
    wait = WebDriverWait(chrome, 5)

    search = find(wait, 'input.input_text')
    search.send_keys(f'{emotion}\n')

    idx = random.randint(1, 3)
    playlist = find(
        wait, f'#djPlylstList > div > ul > li:nth-child({idx}) > div.thumb')
    playlist.click()

    titles = []
    singers = []
    for i in range(1, 11):
        title = find(
            wait, f'#frm > div > table > tbody > tr:nth-child({i}) > td:nth-child(5) > div > div > div.ellipsis.rank01 > span > a')
        singer = find(
            wait, f'#frm > div > table > tbody > tr:nth-child({i}) > td:nth-child(5) > div > div > div.ellipsis.rank02 > a')
        titles.append(title.text)
        singers.append(singer.text)

    chrome.close()
    return titles, singers

# ua = UserAgent()
# headers = {
#     'User-agent': ua.ie,
#     'referer': 'https://www.melon.com',
# }
# res = req.get(url, headers=headers)
# soup = BS()
# print(res.text)
