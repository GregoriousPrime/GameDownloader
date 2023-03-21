#a script that downloads cracked games from STEAMRIP / GOG.

import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import webbrowser
from constants import *


def main():
  
  def search_in_gog(game_name = None, page = 1):

    game_name = game_name.replace(' ', '-').lower()

    response = requests.get(f'{gog_list}{game_name}/{page}{gog_addon}')
    soup = BeautifulSoup(response.content, 'html.parser')
    game_html_line = soup.find_all('a', {'class': 'block'})

    if len(game_html_line) > 1:
      
      for i, game in enumerate(game_html_line):

        title = game.text
        title = re.sub(r'\s*Last Update.*', '', title).strip()  
        print(f'{i+1}. {title}') 

        if (i+1) % 28 == 0:

          question = input('Do you want to continue to the next page? Answer with y / n. ')

          if question == 'y':
            
            print(f'question = {question}')
            page += 1
            search_in_gog(game_name, page)

          else:
            break
          
      question = int(input('\nYou have multiple options, please pick the one you want: \nif the game you want is not in the list type \'999\':\n')) - 1
      
      if question == 998:
        game_url = search_in_steamrip(game_name)
        
        return game_url
      
      elif question >= len(game_html_line):
        question = int(input('\nThe number you chose was not in the list, Please choose again: \n')) - 1

      href_value = game_html_line[question].get('href')
      game_url = f'https://gog-games.com{href_value}'

      return game_url
    
    elif len(game_html_line) == 0:
      game_url = search_in_steamrip(game_name)

      return game_url

    href_value = game_html_line[0].get('href')
    game_url = f'https://gog-games.com{href_value}'

    return game_url

  def search_in_steamrip(game_name = None):

    if game_name == None:
      game_name = input('Please input the game\'s name: \n')
    
    game_name = game_name.replace(' ', '-').lower()

    response = requests.get(gamelist1)
    soup = BeautifulSoup(response.content, 'html.parser')
    game_html_line = soup.find_all('a', href=re.compile(game_name))

    if len(game_html_line) > 1:
      i = 0

      for i, game in enumerate(game_html_line):
        title = game.text
        print(f'{i+1}. {title}')

      question = int(input('\nYou have multiple options, please pick the one you want: ')) - 1

      if question >= len(game_html_line):
          question = int(input('\nThe number you chose was not in the list, Please choose again: \n')) - 1

      href_value = game_html_line[question].get('href')
      game_url = f'https://webcache.googleusercontent.com/search?q=cache:https://steamrip.com{href_value}'

      return game_url
    
    elif len(game_html_line) == 0:
      print('Couldn\'t find the game you asked for, Please try again.')

      return None

    href_value = game_html_line[0].get('href')
    game_url = f'https://webcache.googleusercontent.com/search?q=cache:https://steamrip.com{href_value}'

    return game_url

  def find_and_download(game_url):

    if game_url == None:
      return None
    
    response = requests.get(game_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if game_url.find('steamrip.com') > 0:
      download_html_line = soup.find('a', class_="shortc-button medium purple")

      if download_html_line == None:
        index_cash = game_url.find('cache:') + 6
        actual_url = game_url[index_cash:]

        print('Failed to find the link to the download in ' + actual_url)
        return None
      
      url = download_html_line.get('href')[2:]
      formatted_url = f'https://{url}'
      webbrowser.open(formatted_url)
            
    else:
      driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
      driver.get(game_url)
      driver.find_element(By.CLASS_NAME, "g-recaptcha").click()
      wait = WebDriverWait(driver, 50)
      wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="game-details"]/div/div[2]/div[1]/div[1]')))
      html = driver.page_source
      download_link = re.search(r'(filecrypt\.cc\/Container\/\w+)', html)

      if download_link:
        formatted_url = f'https://{download_link.group(1)}'
        driver.get(formatted_url)
        wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="cnl_btn"]')))
        driver.find_element(By.XPATH, '//*[@id="cnl_btn"]').click()
        sleep(55)

      else:
        download_link = re.search(r'(?:title=")(https:\/\/1fichier\..*)(?:" href)', html)
        if download_link:
          formatted_url = f'https://{download_link.group(1)}'

  



  game_name = input('Please input the game\'s name: \n')

  find_and_download(search_in_gog(game_name))

if __name__ == '__main__':
  main()
  

