# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from tqdm import tqdm

import config_vote as config
# import teste as config

# %%
print(config.candidates)

# %%
def init_driver(silent=False): #silent abre sem interface visual
    options = webdriver.ChromeOptions()
    
    if silent:
        options.add_argument("headless")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    return driver

# %%
def verify_candidates(driver, link, candidates):
    driver.get(link)
    for animal in candidates:
        print(animal)
        animal_button = driver.find_element(by=By.XPATH, value=f"//*[contains(text(), {animal})]")
        animal_button.click()
        time.sleep(5) # x seconds

# %%
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

	# print("Done!")

# %%
if __name__ == "__main__":
    QUIET=True

    vote_list = config.candidates

    driver = init_driver(silent=QUIET)
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
            driver = init_driver(silent=QUIET)

# %%
# driver = init_driver(silent=False)
# verify_candidates(driver, config.base_url, config.candidates)


