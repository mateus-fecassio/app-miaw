from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


# def init_driver(silent=False): #silent abre sem interface visual
#     options = webdriver.ChromeOptions()
    
#     if silent:
#         options.add_argument("headless")

#     try:
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     except:
#         driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

#     return driver


def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    return driver


def votation(driver, link, person_xpath, vote_counter):
	# vote_count = random.randint(10,30)
	vote_count = 1
	
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


if __name__ == "__main__":
    QUIET=True

    vote_counter = [0]

    link = 'https://miaw.mtv.com.br/vote/streamer-br'
    person_xpath = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[33]/div/div/div[3]/div/div[5]/div/button' # samira

    driver = init_driver(silent=QUIET)
    while True:
        try:
            votation(driver, link, person_xpath, vote_counter)

            text = f'NOTE: {vote_counter[0]} votes submitted so far.\n'
            print(text)
        except:
            text = f'ERROR: Quiting and restarting driver... The last vote_counter was {vote_counter[0]}\n'
            print(text)

            time.sleep(60) # x seconds
            driver.quit()
            driver = init_driver(silent=QUIET)
            # driver.refresh()

        try:
            driver.refresh()
        except:
            pass