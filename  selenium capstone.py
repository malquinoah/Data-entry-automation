from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

GOOGLE_FORM = ('https://docs.google.com/forms/d/e/1FAIpQLSfY_bjteOvhnV26hvKHw6Lvlf2JP-gvPQmOoMoooHuMpYNhGg/viewform'
               '?usp=sf_link')
FAKE_ZILLOW = 'https://appbrewery.github.io/Zillow-Clone/'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

response = requests.get(FAKE_ZILLOW)

soup = BeautifulSoup(response.text, 'html.parser')

home_prices = soup.select('div span.PropertyCardWrapper__StyledPriceLine')
home_links = soup.select('div a.StyledPropertyCardDataArea-anchor')
home_addresses = soup.select('address')

prices = []
links = []
addresses = []

for home in home_prices:
    price = home.text.split('/')[0]
    price = price.split('+')[0]
    prices.append(price)

for home in home_links:
    link = home.get('href')
    links.append(link)

for home in home_addresses:
    addresses.append(home.text.strip().replace('|', ''))

for _ in range(len(prices)):
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(GOOGLE_FORM)
    driver.maximize_window()

    q1 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div['
                                       '1]/input')
    q1.send_keys(addresses[_])

    q2 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div['
                                       '1]/input')
    q2.send_keys(prices[_])

    q3 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div['
                                       '1]/input')
    q3.send_keys(links[_])
    time.sleep(1)

    submit = driver.find_element(By.CSS_SELECTOR, 'span.NPEfkd')
    submit.click()

    driver.close()
print('done')
