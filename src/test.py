import os
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
import undetected_chromedriver as uc


if __name__ == "__main__":


    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = uc.Chrome(use_subprocess=False, headless=False)

    # stealth(driver,
    #         languages=["en-US", "en"],
    #         vendor="Google Inc.",
    #         platform="macOS",
    #         webgl_vendor="Intel Inc.",
    #         renderer="Intel Iris OpenGL Engine",
    #         fix_hairline=True,
    #         )

    # url = "https://bot.sannysoft.com/"
    # driver.get(url)
    # time.sleep(5)
    # driver.save_screenshot("sannysoft.png")
    # driver.quit()

    # browser = webdriver.Chrome()
    driver.get('https://solscan.io/account/9WiFm4KzEbMvn1HQBVMb4W49S9rNfqhqjK9sjXJqiCbQ#defiactivities')
    driver.implicitly_wait(5)
    defi = driver.find_element(By.ID, 'account-tabs')
    print(defi)
