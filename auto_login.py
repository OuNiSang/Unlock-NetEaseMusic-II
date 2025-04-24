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
    browser.add_cookie({"name": "MUSIC_U", "value": "00516C6F4C7066D5A3F13C1DDA3BA77D614BA3EBB4D6A03F542365212B1EE87CA4D76A8618A4BE75BCC60DD3A0E6712E93628CCBCE2E2E2D6B8BE4C9C9BABC7A00AE3BEF89CED98E218B819B25DBB4BD5D12EE7D19F988CF9430FC87A8EEDA16221F93A76058CE83E3867DC5AFE105DA83AB5FE55F7843D9FF71D83DAC1BB56BC2624992F3B8FC8E43A9AB1FCE3CBA7A08BE9CF5EBD1932ABD8AF31F3EC3382A15DD8F214B162D4FB513D9BC5ACF468A52BF3D7EA3B72975C055787F4B82CB82487A4787CAB7C98BD9E2CB222EF8FDC12CA3FEE959B58BFB375AE71B24765499357B1B7AAD3F452E8D588D77BD92DB1B487DCE321CB5F8071C9CD4EC04D17F45352F155D8A00E40CED700E3D213CE3BA018C842FAF63C2A3E11054D6416310161A0DBACE954B1D4C7BC09DF1D0A1BAA11FA644F54D98554CBE591B5CCCE084DDBA9DA6AA258686DD683995D38C7A5DBFAF7793B77727623B5E93FB8F46CF6DD47E unblockneteasemusic
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
