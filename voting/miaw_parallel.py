from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from os import environ
from threading import Thread
import gc



# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
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
    chrome_options.binary_location = environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    return driver


def votation(driver, link, person_xpath, vote_counter):
    driver.get(link)
    sleep(12) # x seconds
    for _ in range(20):	
        for _ in range(10):
            try:
                driver.find_element(by=By.XPATH, value=person_xpath).click()
                vote_counter[0] += 1
            except:
                pass
            sleep(0.1) # x seconds
        
        sleep(11) # x seconds
        driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/div/div[2]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div[3]/div/div').click()
        gc.collect()
    
    # print("Done!")

def main(th=0):
    print(f'Thread {th} -- OK')

    sleep(10)
    vote_counter = [0]

    link = 'https://miaw.mtv.com.br/vote/streamer-br'
    person_xpath = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[33]/div/div/div[3]/div/div[5]/div/button' # samira

    driver = init_driver()
    gc.collect()

    while True:
        try:
            votation(driver, link, person_xpath, vote_counter)

            print(f'Thread {th} -- NOTE: {vote_counter[0]} votes submitted so far.')
            gc.collect()
        except:
            print(f'Thread {th} -- ERROR: Quiting and restarting driver... The last vote_counter was {vote_counter[0]}')
            gc.collect()

            sleep(60) # x seconds
            driver.quit()
            driver = init_driver()
            # driver.refresh()

        try:
            driver.refresh()
        except:
            pass
        
        gc.collect()

if __name__ == "__main__":
    for th in range(2):
        Thread(target=main, args=([th])).start()
    # main()