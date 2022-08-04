from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
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

def create_tabs(driver, link, number=3):
    tab_list = []

    driver.get(link)
    tab_list.append(driver.current_window_handle)
    
    if number > 0:
        for i in range(number):
            script = f"window.open('about:blank', 'tab{i}');"

            driver.execute_script(script)
            driver.switch_to.window(f'tab{i}')

            driver.get(link)
            tab_list.append(driver.current_window_handle)

            time.sleep(5)

        driver.switch_to.window(tab_list[0])

    time.sleep(20)
    return tab_list


def votation_tab(driver, link, person_xpath, vote_counter, tab_list):
    # vote_count = random.randint(10,30)
    vote_count = 20
    
    # driver.get(link)
    # time.sleep(10) # x seconds
    for _ in range(vote_count):
        for tab in tab_list:
            driver.switch_to.window(tab)
            time.sleep(2) # x seconds
            for _ in range(10):
                try:
                    driver.find_element(by=By.XPATH, value=person_xpath).click()
                    vote_counter[0] += 1
                except:
                    pass
                time.sleep(1) # x seconds
            
        time.sleep(11) # x seconds
        for tab in tab_list:
            try:
                driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/div/div[2]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div[3]/div/div').click()
            except:
                pass
            time.sleep(1) # x seconds
        time.sleep(2) # x seconds


def votation(driver, link, person_xpath, vote_counter):
    # vote_count = random.randint(10,30)
    vote_count = 20
    
    driver.get(link)
    time.sleep(10) # x seconds
    for _ in range(vote_count):
        # time.sleep(2) # x seconds
        
        for _ in range(10):
            try:
                driver.find_element(by=By.XPATH, value=person_xpath).click()
                vote_counter[0] += 1
            except:
                pass
            time.sleep(0.1) # x seconds
        
        time.sleep(11) # x seconds
        driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/div/div[2]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div[3]/div/div').click()


if __name__ == "__main__":
    vote_counter = [0]

    link = 'https://miaw.mtv.com.br/vote/streamer-br'
    person_xpath = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[33]/div/div/div[3]/div/div[5]/div/button' # samira

    driver = init_driver()
    # tab_list = create_tabs(driver, link)

    # for _ in range(2):
    while True:
        try:
            votation(driver, link, person_xpath, vote_counter)

            text = f'NOTE: {vote_counter[0]} votes submitted so far.'
            print(text)
        except:
            text = f'ERROR: Quiting and restarting driver... The last vote_counter was {vote_counter[0]}.'
            print(text)

            time.sleep(60) # x seconds
            driver.quit()
            driver = init_driver()
            # driver.refresh()

        try:
            driver.refresh()
        except:
            pass