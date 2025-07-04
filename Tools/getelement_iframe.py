from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook, load_workbook
from List_Zentao import ID
from PIL import ImageGrab
import time
import pyautogui

# Launch Excel Database
wb = load_workbook('Night Database.xlsx')
ws = wb.active

def main():

    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=\\Users\\n02-19\\Library\\Application Support\\Google\\Chrome\\')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36")
    options.add_argument('profile-directory=Default')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless flag')
    options.add_argument('start-maximized') 
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_experimental_option('excludeSwitches', ['enable-automation','enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    driver =webdriver.Chrome(options=options)

    # webdriver防屏蔽
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
       Object.defineProperty(navigator, 'webdriver', {
         get: () => false
       })
     """    
    })
    baidu(driver)
    driver.quit()


def wait(driver, path, text):
    try:
        WebDriverWait(driver, 100).until(EC.text_to_be_present_in_element((By.XPATH, path), text))
    except:
        pass

# Gname
def baidu(driver):


    # Go to Webpage
    driver.get('https://account.alibabacloud.com/login/login.htm?oauth_callback=https%3A%2F%2Fhome-intl.console.aliyun.com%2F')

    time.sleep(5)

    # Drag and Drop Appear?
    if pyautogui.locateOnScreen('./image/alidnd.png') is not None:
        driver.switch_to.frame("alibaba-login-box")
        driver.switch_to.frame("baxia-dialog-content")
        slider = driver.find_element(By.XPATH, '/html/body/center/div[1]/div/div/div/span')
        print(slider)
        action_chains = ActionChains(driver)
        action_chains.move_to_element(slider)
        action_chains.click_and_hold()
        action_chains.move_by_offset(360, 0)
        action_chains.release()
        action_chains.perform()

        time.sleep(111111)

    else:
        pass

        
if __name__ == "__main__":
    main()
