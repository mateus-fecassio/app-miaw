from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time



def init_driver(silent=False): #silent abre sem interface visual
    options = webdriver.ChromeOptions()
    
    if silent:
        # options.add_argument("headless")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    return driver


def votation(driver, link, person_xpath, vote_counter):
	# vote_count = random.randint(10,30)
	vote_count = 20
	
	driver.get(link)
	time.sleep(12) # x seconds
	for _ in range(vote_count):
		# time.sleep(2) # x seconds
		
		for _ in range(10):
			try:
				send_button = driver.find_element(by=By.XPATH, value=person_xpath)
				send_button.click()
				vote_counter[0] += 1
			except:
				pass
			time.sleep(0.1) # x seconds
		
		time.sleep(11) # x seconds
		conf_button = driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/div/div[2]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div[3]/div/div')
		conf_button.click()
	
	# print("Done!")



def main(th=0):
    print(f'Thread {th} -- OK')
    time.sleep(2) # x seconds
    QUIET=True

    # arquivo de LOG
    # FILEPATH = os.path.join(os.getcwd(), 'LOGS_miaw')
    # if not os.path.exists(FILEPATH):
    #     os.mkdir(FILEPATH)
    # PROGNAME = 'mtv_miaw'
    # FILENAME = os.path.join(FILEPATH, f'{PROGNAME}.txt')

    vote_counter = [0]

    link = 'https://miaw.mtv.com.br/vote/streamer-br'
    person_xpath = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[33]/div/div/div[3]/div/div[5]/div/button' # samira

    driver = init_driver(silent=QUIET)
    time.sleep(30) # x seconds
    while True:
        # file = open(FILENAME, 'a', encoding='utf-8')


        try:
            votation(driver, link, person_xpath, vote_counter)

            text = f'Thread {th} -- NOTE: {vote_counter[0]} votes submitted so far.'
            print(text)
            # file.write(text)
        except:
            text = f'Thread {th} -- ERROR: Quiting and restarting driver... The last vote_counter was {vote_counter[0]}'
            print(text)
            # file.write(text)

            time.sleep(60) # x seconds
            driver.quit()
            driver = init_driver(silent=QUIET)
            # driver.refresh()

        try:
            driver.refresh()
            # file.close()
        except:
            pass