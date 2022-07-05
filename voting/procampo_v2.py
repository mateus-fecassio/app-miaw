from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from tqdm import tqdm
import os

import config_vote as config
# import teste as config


def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    return driver

def verify_candidates(driver, link, candidates):
    driver.get(link)
    for animal in candidates:
        print(animal)
        animal_button = driver.find_element(by=By.XPATH, value=f"//*[contains(text(), {animal})]")
        animal_button.click()
        time.sleep(5) # x seconds


def votation(driver, link, candidates, email_list, vote_counter):
	for email in email_list:
		
		VOTE_LIMIT = 30
		for _ in tqdm(range(VOTE_LIMIT)):
			for animal in candidates:
				driver.get(link)
			
				time.sleep(2) # x seconds

				# preencher e-mail, se precisar
				try:
					email_field = driver.find_element(by=By.XPATH, value=config.email_xpath)
					email_field.send_keys(email)
				except:
					print('E-mail não é preciso mais? Verificar!')
					pass
				
				time.sleep(0.5) # x seconds
			
				# animal
				animal_button = driver.find_element(by=By.XPATH, value=f"//*[contains(text(), {animal})]")
				animal_button.click()

				time.sleep(0.5) # x seconds

				# botão de enviar
				send_button = driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'Enviar')]")
				send_button.click()

				time.sleep(0.5) # x seconds
				vote_counter[1] += 1

			vote_counter[0] += 1
		
		# print(f'Voting using e-mail: {email} - FINISHED. Refreshing...')
		driver.refresh() #limpa a memória e impede erro por falta de memória


if __name__ == "__main__":
    vote_list = config.candidates

    driver = init_driver()
    vote_counter = [0, 0]
    i = 0

    while True:
        try:
            i += 1
            print(f'Round {i}, fight!')
            votation(driver, config.base_url, vote_list, config.emails, vote_counter)
            print(f'NOTE: {vote_counter[0]} votes submitted so far for each candidate. Total votes: {vote_counter[1]}')
        except Exception as e:
            print(e)
            print('Quiting and rebooting driver...')
            driver.quit()
            driver = init_driver()
