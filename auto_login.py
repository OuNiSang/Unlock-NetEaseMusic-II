# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "006FB48AAB7130C64E49DC8FD5A8D333E2A4104DB29B6EA48477400D57947FEF3692C019FDF7FF0ADCA1F981D255D4A7D413D5BFF7C766B63729AF3EEE2D1A88DF4AA1207C63E2DFB6A06323F6B56B990EB26B2B639709FE51B9DDBC99A37CE7A016C9A01C952CE003EB091F5E409B0446A6FEB706C056DAA260D32D2F40E9763824636AE36A1B518564168D73DC937DE5E029E2C610037355DE98B41084006074B852EF940C839816ADF14FD4F58D969532B72153BBBD775EF5D607A4DCF8A461E5DC5CC5C070AB5CD11C1B6B1AC68EABEAB8181666AB7BD96CD043D3A892DB8E2193C63B8E677722C6B8FCEC491E53A24F7E4AC4B8188193D7FE4C43E7CE4B27C40D191FB92AF00CBEDA9AEABD73E192F3D827F84F7D5F2DCD017F402FB23736E9258A1CBFF38E0EEFF09C801C74D4058263D3B56873762483D35B79B0C647386E58B2BA171E2FCCBCB9D3DAA2FA5D4D1D23FD7710D63FFFE3731DC3D4959C27
`"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
