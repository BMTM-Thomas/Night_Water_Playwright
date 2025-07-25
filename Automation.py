import re
import os
import time
import atexit
import base64
import random
import certifi
import logging
import requests
import pyautogui
import pyperclip
import subprocess
from List_Zentao import *
from openai import OpenAI
from bson import ObjectId 
from List_Noctool import *
from selenium import webdriver  
from dotenv import load_dotenv
from pymongo import MongoClient
from PIL import ImageGrab
from bson.objectid import ObjectId  
from List_Aliyun_DDCaptcha import *   
from AppKit import NSPasteboard, NSPasteboardTypePNG
from playwright.sync_api import sync_playwright, expect

# OpenAI API
class MyChatGPT:
    """OpenAI GPT-4o API Client""" 

    # OpenAI API Client Initialization
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    # Convert image to base64 
    def image_file_to_base64(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    # Step 1: Ask GPT-4o to analyze the image and read instruction 
    def ask_gpt_about_image(self, image_path, prompt_text):
        base64_img = self.image_file_to_base64(image_path)

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        { "type": "text", "text": prompt_text },
                        { "type": "image_url", "image_url": { "url": f"data:image/png;base64,{base64_img}" } }
                    ]
                }
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    # Step 2: Auto click tiles based on GPT response
    def extract_positions_and_click(self, response_text):

        # Random Time Sleep
        random_Sleep = random.uniform(0.5, 1)  # Random sleep between 0.5 to 1 second

        GRID_MAP = {
            "1-1": (703,441),
            "1-2": (787,435),
            "1-3": (938,427),
            "2-1": (685,559),
            "2-2": (789,534),
            "2-3": (947,574),
        }
        
        positions = re.findall(r"\d-\d", response_text)
        for pos in positions:
            if pos in GRID_MAP:
                x, y = GRID_MAP[pos]
                print(f"Clicking {pos} at ({x}, {y})")
                # Random time sleep between 0.5 to 1 second
                # time.sleep(random_Sleep)
                pyautogui.click(x, y)  
                # Random time sleep between 0.5 to 1 second
                # time.sleep(random_Sleep)
            else:
                print(f"[!] Unknown position: {pos}")

# Logging Setup
class Logger:
    """Enhanced logging setup"""
    
    @staticmethod
    def setup_logger(name: str = "aliyun_automation", level: int = logging.INFO) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        if not logger.handlers:
            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            
            # Create file handler
            file_handler = logging.FileHandler('automation.log')
            file_handler.setLevel(level)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
        
        return logger

# Javascript element color
class JavaScript_Style:

    @staticmethod
    def red_Check(locator, text):
        locator.evaluate(f"""
            (e) => {{
                e.style.border = '3px solid red';
                e.style.position = 'relative';

                const existing = document.getElementById('floating-label');
                if (existing) existing.remove();

                const rect = e.getBoundingClientRect();

                const label = document.createElement('div');
                label.id = 'floating-label';
                label.innerText = "{text}";
                label.style.position = 'fixed';
                label.style.top = (rect.top - 25) + 'px';
                label.style.left = rect.left + 'px';
                label.style.backgroundColor = 'red';
                label.style.color = 'white';
                label.style.padding = '2px 6px';
                label.style.fontSize = '12px';
                label.style.zIndex = '9999';
                label.style.fontFamily = 'Arial, sans-serif';
                label.style.fontWeight = 'bold';

                document.body.appendChild(label);
            }}
        """)

    @staticmethod
    def green_Check(locator, text):
        locator.evaluate(f"""
            (e) => {{
                e.style.border = '3px solid green';

                const label = document.getElementById('floating-label');
                if (label) {{
                    label.innerText = "{text}";
                    label.style.backgroundColor = 'green';
                    label.style.border = '1px solid green';
                }}
            }}
        """)
        
    @staticmethod
    def mouse_red_dot(page, x, y):

        page.evaluate("""
            ([x, y]) => {
                let el = document.createElement('div');
                el.style.position = 'absolute';
                el.style.left = x + 'px';
                el.style.top = y + 'px';
                el.style.width = '20px';
                el.style.height = '20px';
                el.style.background = 'red';
                el.style.borderRadius = '50%';
                el.style.zIndex = 9999;
                el.style.pointerEvents = 'none';
                document.body.appendChild(el);
            }
        """, [x, y])

# Selenium Automation Settings
class Selenium_Automation:
    @staticmethod
    def chrome():
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=\\Users\\Thomas\\Library\\Application Support\\Google\\Chrome\\")
        options.add_argument('profile-directory=Profile 3')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('start-maximized') 
        options.add_argument('--no-default-browser-check')
        options.add_argument('--no-first-run')
        options.add_argument('--hide-crash-restore-bubble')
        options.add_experimental_option('excludeSwitches', ['enable-automation','enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)

        return driver

# Plawright Automation Settings
class Automation:

    # Chrome Extension
    EXTENSION_PATH = "/Users/n02-19/Desktop/playWright/chrome_Extension/lastPass"  # Extension
    EXTENSION_PATH2 = "/Users/n02-19/Desktop/playWright/chrome_Extension/SelectorHub"  # Extension

    # User Profile
    USER_DATA_DIR = "/Users/n02-19/PlaywrightProfile"  # User Profile

    # MongoDB Serverless
    @staticmethod
    def mongodb_atlas():
        
        # Call MongoDB Atlas API Key
        load_dotenv()
        mongodb_api_key = os.getenv("MONGODB_API_KEY")
        
        # MongoDB Atlas (Server)
        client = MongoClient(mongodb_api_key,tlsCAFile=certifi.where())
        # Access Database
        db = client["Thomas"]
        # Access Collection
        return db["Night_Database_2"]
    
        # Chromium Browser (def chromium can delete if no use)
    
    # Chromium Browser
    @classmethod
    def chromium(cls, p):
        browser = p.chromium.launch_persistent_context(
            cls.USER_DATA_DIR,
            headless=False,  # Extensions do NOT work in headless mode
            args=[
                f"--disable-extensions-except={cls.EXTENSION_PATH},{cls.EXTENSION_PATH2}", # Adding Multiple Extensions, dont add any space after "," , else not working
                f"--load-extension={cls.EXTENSION_PATH},{cls.EXTENSION_PATH2}", # Adding Multiple Extensions, dont add any space after "," , else not working
                "--disable-infobars",
                "--disable-blink-features=AutomationControlled",
                "--disable-popup-blocking",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-logging", 
                "--no-sandbox",
                "--start-maximized",
                "--no-default-browser-check",
                "--no-first-run",
                "--hide-crash-restore-bubble",
                "--disable-web-security",
                "--allow-running-insecure-content",
            ],
            no_viewport=True,
            locale="en-US",
        )
        return browser

    # Chrome CDP 
    chrome_proc = None
    @classmethod
    def chrome_CDP(cls):
        # Step 1: Start Chrome normally
        cls.chrome_proc = subprocess.Popen([
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "--remote-debugging-port=9222",
            "--user-data-dir=/Users/n02-19/PlaywrightProfile",
            "--disable-session-crashed-bubble",
            "--hide-crash-restore-bubble",
            "--no-first-run",
            "--no-default-browser-check",
            f"--disable-extensions-except={cls.EXTENSION_PATH},{cls.EXTENSION_PATH2}", # Adding Multiple Extensions, dont add any space after "," , else not working
            f"--load-extension={cls.EXTENSION_PATH},{cls.EXTENSION_PATH2}", # Adding Multiple Extensions, dont add any space after "," , else not working
        ],
        stdout=subprocess.DEVNULL,  # ✅ hide chrome cdp logs
        stderr=subprocess.DEVNULL   # ✅ hide chrome cdp logs
        )
        print("Chrome launched. Waiting...")

        atexit.register(cls.cleanup)

    # Close Chrome CDP
    @classmethod
    def cleanup(cls):
        try:
            print("Gracefully terminating Chrome...")
            cls.chrome_proc.terminate()
        except Exception as e:
            print(f"Error terminating Chrome: {e}")
    
    # Wait for Chrome CDP to be ready
    @staticmethod
    def wait_for_cdp_ready(timeout=10):
        """Wait until Chrome CDP is ready at http://localhost:9222/json"""
        for _ in range(timeout):
            try:
                res = requests.get("http://localhost:9222/json")
                if res.status_code == 200:
                    return True
            except:
                pass
            time.sleep(1)
        raise RuntimeError("Chrome CDP is not ready after waiting.")

# Aliyun Automation
class Aliyun(Automation, JavaScript_Style):

    # Drag n Drop Random Number
    @classmethod
    def drag_random(cls, x, y):
        random_x = random.randint(*x)
        random_y = random.randint(*y)
        pyautogui.moveTo(random_x, random_y, duration=0.15)
        return random_x, random_y
    @classmethod
    def drop_random(cls, x, y):
        random_x = random.randint(*x)
        random_y = random.randint(*y)
        pyautogui.dragTo(random_x, random_y, button='left', duration=0.13)
        return random_x, random_y

    # Aliyun 中国站
    @classmethod
    def aliyun_CN(cls):
        with sync_playwright() as p:  
   
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = cls.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()    

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
            page.goto("https://account.aliyun.com/login/login.htm?oauth_callback=https://usercenter2.aliyun.com/home", wait_until="domcontentloaded", timeout= 0)
            
            # if is "RAM 用户登录" then click "主账号登录", else skip
            try:
                if page.wait_for_selector("//h3[contains(text(),'RAM 用户登录')]", timeout=1000):
                    # Click "主账号登录"
                    page.locator("//span[contains(text(),'主账号登录')]").click()
                    # delay 1second
                    page.wait_for_timeout(1000)
                    # page go to a link
                    page.goto("https://account.aliyun.com/login/login.htm?oauth_callback=https://usercenter2.aliyun.com/home")
            except:
                pass
 
            for ven_id in aliyun_CN_ID:
                
                ## Get iframe
                iframe = page.frame_locator("//div[@id='alibaba-login-iframe']//iframe[@id='alibaba-login-box']")

                ## Wait for "立即登录" to be appear
                __class__.red_Check(iframe.locator("//button[contains(text(),'立即登录')]"), "Wait '立即登录'")
                __class__.green_Check(iframe.locator("//button[contains(text(),'立即登录')]"), "OK! Ready to Click !")

                # click 账号登录 lastpass extension
                pyautogui.click(x=1326, y=383)
                # delay 0.5second
                page.wait_for_timeout(500)
                pyautogui.click(x=1345, y=384)

                # click lastpass extension       
                pyautogui.click(x=1416, y=62)
  
                # Wait for lastpass vault button image to appear
                image_vault = None
                while image_vault is None:
                    image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

                # lastpass search ven and click 
                # delay 0.5second
                page.wait_for_timeout(500)
                pyautogui.write(ven_id)
                # delay 1second
                page.wait_for_timeout(500)
                # Mouse Click
                pyautogui.click(x=1260, y=170)
                # delay 0.5second
                page.wait_for_timeout(500)
            
                ## Click "立即登录" to Login
                iframe.locator('.fm-btn').click()

                # due to ven387 ven407 NEW UI change, ven338 remain old UI
                if ven_id == "ven338":
                    # Wait for "简体中文" 
                    __class__.red_Check(page.locator("//span[@class='sc-jWgTtR leLjBy'][contains(text(),'可用额度')]"), "Wait '可用额度'")
                    __class__.green_Check(page.locator("//span[@class='sc-jWgTtR leLjBy'][contains(text(),'可用额度')]"), "OK!")
                    
                    # Extract Credit
                    __class__.red_Check(page.locator("//span[@class='amount']//span[1]"), "Wait '可用额度'")
                    __class__.green_Check(page.locator("//span[@class='amount']//span[1]"), "Extract Credit")
                    credit = page.locator("//span[@class='amount']//span[1]").text_content() 

                else:
                    # Wait for "账户可用额度"
                    __class__.red_Check(page.locator("//div[@class='label'][contains(text(),'账户可用额度')]"), "Wait '账户可用额度'")
                    __class__.green_Check(page.locator("//div[@class='label'][contains(text(),'账户可用额度')]"), "OK!")

                    try:
                        # wait until the * or "账户可用额度*充值汇款提现汇款认领收支明细详情" disappear
                        expect(page.locator("//div[@id='status-message']")).not_to_have_text("账户可用额度*充值汇款提现汇款认领收支明细详情", timeout=1000)
                    except:
                        pass

                    # Extract Credit
                    __class__.red_Check(page.locator("//div[@id='home-overview-availableAmount']//div[@class='money']"), "Wait '账户可用额度'")
                    __class__.green_Check(page.locator("//div[@id='home-overview-availableAmount']//div[@class='money']"), "Extract Credit!")
                    credit = page.locator("//div[@id='home-overview-availableAmount']//div[@class='money']").text_content() 
    
                # Replace
                credit = credit.replace('¥ ', '')
                credit = credit.replace(',', '')

                # MongoDB Update Data
                mangos_id = {'_id': ObjectId(aliyun_CN_MONGODB[m_id])}
                collection.update_one(mangos_id, {"$set": {"Credit": credit}})
                print(f"{ven_id}= {credit}")
                # mongdb+id +1
                m_id += 1
                
                # Wait for "主账号" to be appear
                __class__.red_Check(page.locator("(//div[@class='sc-taltu8-3 CB-cquEbr'])[1]"), "Wait '主账号'")
                __class__.green_Check(page.locator("(//div[@class='sc-taltu8-3 CB-cquEbr'])[1]"), "OK!")
                
                # hover to menu
                __class__.red_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!'")
                __class__.green_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!'")
                page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # if hover menu doesnt appear, rehover again
                while True:
                    try:
                        # Wait for "权限与安全" to be appear
                        page.locator("//span[contains(text(),'权限与安全')]").wait_for(timeout=1000) 
                        __class__.red_Check(page.locator("//span[contains(text(),'权限与安全')]"), "Wait '权限与安全'")
                        __class__.green_Check(page.locator("//span[contains(text(),'权限与安全')]"), "OK!")
                        break
                    except:
                        # Mouse Click
                        pyautogui.click(x=1267, y=217)
                        # delay 0.5second
                        page.wait_for_timeout(500)
                        # hover to menu
                        __class__.red_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!'")
                        __class__.green_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!'")
                        page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # delay 0.5second
                page.wait_for_timeout(500)

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # Click "退出登录" Logout
                __class__.red_Check(page.locator("//a[contains(text(),'退出登录')]"), "退出登录")
                __class__.green_Check(page.locator("//a[contains(text(),'退出登录')]"), "退出登录")
                page.locator("//a[contains(text(),'退出登录')]").click(force=True)

                # delay 3seconds
                page.wait_for_timeout(3000)

                page.goto("https://account.aliyun.com/login/login.htm?oauth_callback=https://usercenter2.aliyun.com/home", wait_until="domcontentloaded", timeout= 0)

                # delay 3seconds
                page.wait_for_timeout(3000)
    
    # Aliyun 国际站
    @classmethod
    def aliyun_INT(cls):
        with sync_playwright() as p: 
            
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = cls.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
            page.goto("https://account.alibabacloud.com/login/login.htm?oauth_callback=https%3A%2F%2Fusercenter2-intl.console.alibabacloud.com%2Fbilling%2F#/account/overview", wait_until="domcontentloaded")
            
            # if is "RAM 用户登录" then click "主账号登录", else skip
            try:
                if page.wait_for_selector(":has-text('RAM 用户登录')", timeout=2000):
                    # Click "主账号登录"
                    page.locator("//span[contains(text(),'主账号登录')]").click()
                    # delay 0.5second
                    page.wait_for_timeout(500)
                    # page go to a link
                    page.goto("https://account.alibabacloud.com/login/login.htm?oauth_callback=https%3A%2F%2Fusercenter2-intl.console.alibabacloud.com%2Fbilling%2F#/account/overview")
            except:
                pass

            for ven_id in aliyun_INT_ID:
                ## Get iframe
                iframe = page.frame_locator("//iframe[@id='alibaba-login-box']")

                # Wait for "简体中文" to be appear
                __class__.red_Check(page.locator("(//span[contains(text(),'简体中文')])[1]"), "Wait '简体中文'")
                __class__.green_Check(page.locator("(//span[contains(text(),'简体中文')])[1]"), "OK!")

                ## Wait for "登录" to be appear
                __class__.red_Check(iframe.locator("//input[@id='fm-login-submit']"), "Wait '登录'")
                __class__.green_Check(iframe.locator("//input[@id='fm-login-submit']"), "Ready to Click!")
                
                # click lastpass extension       
                pyautogui.click(x=1416, y=62)

                # Wait for lastpass vault button image to appear
                image_vault = None
                while image_vault is None:
                    image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)
  
                # lastpass search ven and click 
                # delay 0.5second
                page.wait_for_timeout(500)
                pyautogui.write(ven_id)
                # delay 0.5second
                page.wait_for_timeout(500)
                # Mouse Click
                pyautogui.click(x=1260, y=170)
                # delay 0.5second
                page.wait_for_timeout(500)

                ## Click "登录" to Login
                iframe.locator('#fm-login-submit').click()

                # Simulate Human move mouse, to prevent bot detect
                cls.drag_random((267, 471), (112, 625))
                
                # delay 3seconds
                page.wait_for_timeout(3000)

                # If Drag and Drop Appear
                while True:
                    #  if image found do something, else will error and stop
                    if pyautogui.locateOnScreen('./image/alidnd.png') is not None:
                    
                        cls.drag_random((975, 1007), (505, 520))
                        cls.drop_random((1255, 1270), (500, 531))

                        # delay 3seconds
                        page.wait_for_timeout(3000)
    
                        # if '登录阿里云账号' is there, means drag and drop failed
                        try:
                            if iframe.locator("//div[@id='login-title']").text_content(timeout=3000) == "登录阿里云账号":
                                # Mouse Click
                                pyautogui.click(x=1114, y=510)
                                # delay 1second
                                page.wait_for_timeout(1000)
                        except:
                            pass
                    else:
                        break
                  
                ## Click "登录" to Login
                try:
                    iframe.locator('#fm-login-submit').click(timeout=500)
                except:
                    pass 

                # Wait "正常" to be appear
                __class__.red_Check(page.locator("//span[contains(text(),'正常')]"), "Wait '正常'")
                __class__.green_Check(page.locator("//span[contains(text(),'正常')]"), "OK!")
                
                # Extract Credit
                __class__.red_Check(page.locator("//div[@class='ng-binding']"), "Extract Credit!")
                __class__.green_Check(page.locator("//div[@class='ng-binding']"), "Extract Credit!")
                credit = page.locator("//div[@class='ng-binding']").text_content()
 
                # Replace
                credit = credit.replace(' USD', '')

                # MongoDB Update Data
                mangos_id = {'_id': ObjectId(aliyun_INT_MONGODB[m_id])}
                collection.update_one(mangos_id, {"$set": {"Credit": credit}})
                print(f"{ven_id}= {credit}")
                # mongdb+id +1
                m_id += 1
                
                # Wait for "主账号" to be appear
                page.locator("(//div[@class='sc-taltu8-3 CB-cquEbr'])[1]").wait_for(timeout=0) 
                __class__.red_Check(page.locator("(//div[@class='sc-taltu8-3 CB-cquEbr'])[1]"), "Wait '主账号'")
                __class__.green_Check(page.locator("(//div[@class='sc-taltu8-3 CB-cquEbr'])[1]"), "OK!")
                
                # delay 0.3second
                page.wait_for_timeout(300)

                # hover to menu
                __class__.red_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!")
                __class__.green_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!")
                page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # if hover menu doesnt appear, rehover again
                while True:
                    try:
                        # Wait for "安全设置" to be appear
                        expect(page.locator("//span[contains(text(),'安全设置')]")).to_be_visible(timeout = 1000) 
                        __class__.red_Check(page.locator("//span[contains(text(),'安全设置')]"), "Wait '安全设置'")
                        __class__.green_Check(page.locator("//span[contains(text(),'安全设置')]"), "OK!")
                        break
                    except:
                        # Mouse Click
                        pyautogui.click(x=1267, y=217)
                        # delay 0.5second
                        page.wait_for_timeout(500)
                        # hover to menu
                        page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # delay 0.3second
                page.wait_for_timeout(300)

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # Click "退出登录" Logout
                __class__.red_Check(page.locator("//a[contains(text(),'退出登录')]"), "退出登录")
                __class__.green_Check(page.locator("//a[contains(text(),'退出登录')]"), "退出登录")
                page.locator("//a[contains(text(),'退出登录')]").click(force=True)
                
                # delay 0.5second
                page.wait_for_timeout(500)

    # Watermelon Aliyun 国际站
    @classmethod
    def watermelon_aliyun_INT(cls):
        with sync_playwright() as p: 
                    
            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
            page.goto("https://account.alibabacloud.com/login/login.htm?oauth_callback=https%3A%2F%2Fusercenter2-intl.console.alibabacloud.com%2Fbilling%2F#/account/overview", wait_until="domcontentloaded")

            # if is "RAM 用户登录" then click "主账号登录", else skip
            try:
                if page.wait_for_selector(":has-text('RAM 用户登录')", timeout=2000):
                    # Click "主账号登录"
                    page.locator("//span[contains(text(),'主账号登录')]").click()
                    # delay 0.5second
                    page.wait_for_timeout(500)
                    # page go to a link
                    page.goto("https://account.alibabacloud.com/login/login.htm?oauth_callback=https%3A%2F%2Fusercenter2-intl.console.alibabacloud.com%2Fbilling%2F#/account/overview")
            except:
                pass

            for ven_id in watermelon_aliyun_INT_ID:
            
                ## Get iframe
                iframe = page.frame_locator("//iframe[@id='alibaba-login-box']")
                # iframe2 = page.frame_locator("iframe#alibaba-login-box") \
                #             .frame_locator("iframe#baxia-dialog-content")

                # Wait for "简体中文" to be appear
                __class__.red_Check(page.locator("(//span[contains(text(),'简体中文')])[1]"), "Wait '简体中文'")
                __class__.green_Check(page.locator("(//span[contains(text(),'简体中文')])[1]"), "OK!")

                ## Wait for "登录" to be appear
                __class__.red_Check(iframe.locator("//input[@id='fm-login-submit']"), "Wait '简体中文'")
                __class__.green_Check(iframe.locator("//input[@id='fm-login-submit']"), "Ready to Click!")
                
                # click lastpass extension       
                pyautogui.click(x=1416, y=63)

                # Wait for lastpass vault button image to appear
                image_vault = None
                while image_vault is None:
                    image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

                # lastpass search ven and click 
                # delay 0.5second
                page.wait_for_timeout(500)
                pyautogui.write(ven_id)
                # delay 0.5second
                page.wait_for_timeout(500)
                # Mouse Click
                pyautogui.click(x=1260, y=170)
                # delay 0.5second
                page.wait_for_timeout(500)

                ## Click "登录" to Login
                iframe.locator('#fm-login-submit').click()

                # Simulate Human move mouse, to prevent bot detect
                cls.drag_random((267, 471), (112, 625))
                
                # delay 3seconds
                page.wait_for_timeout(3000)

                # If Drag and Drop Appear
                while True:
                    #  if image found do something, else will error and stop
                    if pyautogui.locateOnScreen('./image/alidnd.png') is not None:
                    
                        cls.drag_random((975, 1007), (505, 520))
                        cls.drop_random((1255, 1270), (500, 531))

                        # delay 3seconds
                        page.wait_for_timeout(3000)

                        # if '登录阿里云账号' is there, means drag and drop failed
                        try:
                            if iframe.locator("//div[@id='login-title']").text_content(timeout=3000) == "登录阿里云账号":
                                # Mouse Click
                                pyautogui.click(x=1114, y=510)
                                # delay 1second
                                page.wait_for_timeout(1000)
                        except:
                            pass
                    else:
                        break

                ## Click "登录" to Login
                try:
                    iframe.locator('#fm-login-submit').click(timeout=500)
                except:
                    pass    
                
                # Wait "VISA Logo" to be appear
                __class__.red_Check(page.locator("//span[@class='payment-cardrand-visa']"), "Wait 'VISA LOGO APPEAR'")
                __class__.green_Check(page.locator("//span[@class='payment-cardrand-visa']"), "OK!")

                # Check if overdue payment
                try:
                    page.wait_for_selector("//span[@ng-bind-html='item']", timeout=1500)
                    overdue = page.locator("//span[@ng-bind-html='item']").text_content()
                    print(f"{ven_id}= ", overdue)   
                except:
                    pass

                # Screenshot
                ImageGrab.grab().save(f'./watermelon/{ven_id}.png')

                # Wait for "主账号" to be appear
                page.locator("(//div[@class='sc-taltu8-3 CB-cquEbr'])[1]").wait_for(timeout=0) 
                __class__.red_Check(page.locator("(//div[@class='sc-taltu8-3 CB-cquEbr'])[1]"), "Wait '主账号'")
                __class__.green_Check(page.locator("(//div[@class='sc-taltu8-3 CB-cquEbr'])[1]"), "OK!")

                # hover to menu
                __class__.red_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!")
                __class__.green_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!")
                page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # if hover menu doesnt appear, rehover again
                while True:
                    try:
                        # Wait for "安全设置" to be appear
                        expect(page.locator("//span[contains(text(),'安全设置')]")).to_be_visible(timeout = 1000) 
                        __class__.red_Check(page.locator("//span[contains(text(),'安全设置')]"), "Wait '安全设置'")
                        __class__.green_Check(page.locator("//span[contains(text(),'安全设置')]"), "OK!")
                        break
                    except:
                        # Mouse Click
                        pyautogui.click(x=1267, y=217)
                        # delay 0.5second
                        page.wait_for_timeout(500)
                        # hover to menu
                        page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # Wait for "安全设置" to be appear
                expect(page.locator("//span[contains(text(),'安全设置')]")).to_be_visible(timeout = 0) 

                # delay 0.3second
                page.wait_for_timeout(300)

                # Click "退出登录" Logout
                __class__.red_Check(page.locator("//a[contains(text(),'退出登录')]"), "退出登录")
                __class__.green_Check(page.locator("//a[contains(text(),'退出登录')]"), "退出登录")
                page.locator("//a[contains(text(),'退出登录')]").click(force=True)

                # delay 3seconds
                page.wait_for_timeout(3000)

    # Aliyun 国际版【RAM】    # page = gmail, page2 = alibaba
    @classmethod
    def aliyun_INT_RAM(cls):
        with sync_playwright() as p: 
            
            # MongoDB ID
            m_id = 0    

            # Launch MongoDB Atlas
            collection = cls.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()
        
            # Create Browser Tabs
            page = context.pages[0] if context.pages else context.new_page()
            page2 = context.new_page()

            # First Tab Navigate to Gmail
            page.goto("https://mail.google.com/mail/u/0/?ogbl#inbox", wait_until="domcontentloaded")
            # Second Tab Navigate to Aliyun Ram
            page2.goto("https://signin.alibabacloud.com/5256975880117898.onaliyun.com/login.htm?callback=https%3A%2F%2Fusercenter2-intl.aliyun.com%2Fbilling%2F%23%2Faccount%2Foverview#/main", wait_until="domcontentloaded")
            
            # delay 1.5seconds
            page2.wait_for_timeout(1500)

            # Refresh page
            page2.reload()

           # For loop
            for ven_id in aliyun_INT_RAM_ID:
                
                # wait for "RAM 用户登录" to be appear
                __class__.red_Check(page2.locator("//h3[contains(text(),'RAM 用户登录')]"), "Wait 'RAM 用户登录'")
                __class__.green_Check(page2.locator("//h3[contains(text(),'RAM 用户登录')]"), "OK!")
        
                # Wait for lastpass vault button image to appear
                image_vault_0 = None
                while image_vault_0 is None:
                    image_vault_0 = pyautogui.locateOnScreen("./image/vault_0.png", grayscale = True)

                # click lastpass extension       
                pyautogui.click(x=1416, y=63)

                # Wait for lastpass vault button image to appear
                image_vault = None
                while image_vault is None:
                    image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

                # lastpass search ven and click 
                # delay 0.5second
                page2.wait_for_timeout(500)
                pyautogui.write(ven_id)
                # delay 0.5second
                page2.wait_for_timeout(500)
                # Mouse Click
                pyautogui.click(x=1260, y=170)
                # delay 0.5second
                page2.wait_for_timeout(500)

                # Click "下一步" 
                __class__.red_Check(page2.locator("//button[@type='button']"), "Wait '下一步'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//button[@type='button']"), "OK! Click 下一步")
                page2.locator('//button[@type="button"]').click()
                
                # Wait for "*用户密码" appear
                __class__.red_Check(page2.locator("//label[contains(text(),'用户密码')]"), "Wait '*用户密码'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//label[contains(text(),'用户密码')]"), "OK!")

                # delay 0.3second
                page2.wait_for_timeout(300)

                # Click “登入”
                __class__.red_Check(page2.locator("//button[@type='submit']"), "Wait '*用户密码'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//button[@type='submit']"), "OK!")
                page2.locator('//button[@type="submit"]').click()
                
                # delay 0.3second
                page2.wait_for_timeout(300)

                # Wait for "验证安全邮箱" appear
                __class__.red_Check(page2.locator("//h3[contains(text(),'验证安全邮箱')]"), "Wait '验证安全邮箱'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//h3[contains(text(),'验证安全邮箱')]"), "OK!")

                # Click "获取验证码" 
                __class__.red_Check(page2.locator("//span[contains(text(),'获取验证码')]"), "Wait '验证安全邮箱'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//span[contains(text(),'获取验证码')]"), "OK!")
                page2.locator('//span[contains(text(),"获取验证码")]').click()

                # Switch to Gmail
                page.bring_to_front()  

                # 等待gmail alibaba验证码 跳出
                try:
                    while True:
                        try:
                            # Wait until at least one unread email is visible
                            page.wait_for_selector("tr.zE:has-text('Alibaba Cloud'):has-text('Security Verification Code'):has-text('- This email is sent by Alibaba Cloud and is automatically generated. Please do not reply directly. ')", timeout=5000)
                            break
                        except:
                            # Mail Refresh
                            page.locator('//div[@aria-label="Refresh"]//div[@class="asa"]').click()
                            continue
                    
                    # Check first 5 unread email rows
                    for i in range(5):
                        try:
                            row = page.locator("tr.zE").nth(i)
                            content = row.inner_text(timeout=3000)

                            if ("Alibaba Cloud" in content and 
                                "Security Verification Code" in content and 
                                "This email is sent by Alibaba Cloud" in content):
                                row.click()
                                break
                        except Exception as e:
                            continue  # Skip if row not available or timeout

                except TimeoutError:
                    print("No unread Alibaba Cloud email appeared in time.")

                # wait for ""1.  This code is required to complete your account verification or secure login process.""
                page.locator("//p[contains(text(),'1.  This code is required to complete your account')]").wait_for(timeout=0)

                # Regex to remove the unnecessary text, and keep only verification code
                v_code = page.locator("//tbody//tr//p[2]").text_content()
                v_code = re.search(r"Your verification code is:\s*(\d+)", v_code)
                v_code = v_code.group(1)

                # remove whitespace
                v_code = v_code.strip()
                print(f"Alibaba Verification Code: {v_code}")

                # delay 1second
                page.wait_for_timeout(1000)  

                # Click gmail “inbox”
                page.locator('(//div[@class="aio UKr6le"])[1]').click()
                
                # Switch to alibaba tab
                page2.bring_to_front()  

                # delay 1second
                page2.wait_for_timeout(1000) 

                # Wait for "验证安全邮箱" to be appear
                __class__.red_Check(page2.locator("//h3[contains(text(),'验证安全邮箱')]"), "Wait '验证安全邮箱'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//h3[contains(text(),'验证安全邮箱')]"), "OK!")

                # Click "x mark"
                page2.locator('//i[@class="next-icon next-icon-close next-xs"]').click()
                
                # Fill Verification Code
                page2.fill("//input[@id='EMAIL_CODE']", v_code)

                # delay 0.5second
                page2.wait_for_timeout(500) 

                # Click "提交验证码"
                page2.locator('//button[@type="submit"]').click()
                __class__.green_Check(page2.locator("//button[@type='submit']"), "提交验证码")

                # Wait for "正常" appear
                __class__.red_Check(page2.locator("//span[contains(text(),'正常')]"), "Wait '正常'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//span[contains(text(),'正常')]"), "OK!")

                # Mouse Click
                pyautogui.click(x=1100, y=287)
                
                # Extract Credit
                credit = page2.locator(f"//div[@class='ng-binding']").text_content()
                __class__.green_Check(page2.locator("//div[@class='ng-binding']"), "Extract Credit!")

                # Replace
                credit = credit.replace(' USD', '')

                # MongoDB Update Data
                mangos_id = {'_id': ObjectId(aliyun_INT_RAM_MONGODB[m_id])}
                collection.update_one(mangos_id, {"$set": {"Credit": credit}})
                print(f"{ven_id}= {credit}\n")
                # mongdb+id +1
                m_id += 1

                # Wait for "RAM 用户" to be appear
                __class__.red_Check(page2.locator("(//div[@class='sc-taltu8-3 CB-cquEbr'])[1]"), "Wait 'RAM 用户'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("(//div[@class='sc-taltu8-3 CB-cquEbr'])[1]"), "OK!")

                # delay 0.3second
                page2.wait_for_timeout(300)

                # hover to menu
                __class__.red_Check(page2.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!")
                page2.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # if hover menu doesnt appear, rehover again
                while True:
                    try:
                        # Wait for "安全管控" to be appear
                        expect(page2.locator("//span[contains(text(),'安全管控')]")).to_be_visible(timeout = 1000) 
                        __class__.red_Check(page2.locator("//span[contains(text(),'安全管控')]"), "Wait '安全管控'")
                        page2.wait_for_timeout(300)
                        __class__.green_Check(page2.locator("//span[contains(text(),'安全管控')]"), "OK!")
                        break
                    except:
                        # Mouse Click
                        pyautogui.click(x=1267, y=217)
                        # delay 0.3second
                        page2.wait_for_timeout(300)
                        # hover to menu
                        page2.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # delay 0.3second
                page2.wait_for_timeout(500)

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # Click "退出登录" Logout
                __class__.red_Check(page2.locator("//a[contains(text(),'退出登录')]"), "Wait '退出登录'")
                page.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//a[contains(text(),'退出登录')]"), "OK!")
                # 登出
                page2.locator("//a[contains(text(),'退出登录')]").click(force=True)

                # delay 0.5second
                page2.wait_for_timeout(500)

    # Watermelon Aliyun 国际站【RAM】    # page = gmail, page2 = alibaba
    @classmethod
    def watermelon_aliyun_INT_RAM(cls):
        with sync_playwright() as p: 
             
            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Create Browser Tabs
            page = context.pages[0] if context.pages else context.new_page()
            page2 = context.new_page()

            # First Tab Navigate to Gmail
            page.goto("https://mail.google.com/mail/u/0/?ogbl#inbox", wait_until="domcontentloaded")
            # Second Tab Navigate to Aliyun Ram
            page2.goto("https://signin.alibabacloud.com/5256975880117898.onaliyun.com/login.htm?callback=https%3A%2F%2Fusercenter2-intl.aliyun.com%2Fbilling%2F%23%2Faccount%2Foverview#/main", wait_until="domcontentloaded")
            
            # delay 1.5seconds
            page2.wait_for_timeout(1500)

            # Refresh page
            page2.reload()

           # For loop
            for ven_id in watermelon_aliyun_INT_RAM_ID:
                
                # wait for "RAM 用户登录" to be appear
                __class__.red_Check(page2.locator("//h3[contains(text(),'RAM 用户登录')]"), "Wait 'RAM 用户登录'")
                __class__.green_Check(page2.locator("//h3[contains(text(),'RAM 用户登录')]"), "OK!")
        
                # Wait for lastpass vault button image to appear
                image_vault_0 = None
                while image_vault_0 is None:
                    image_vault_0 = pyautogui.locateOnScreen("./image/vault_0.png", grayscale = True)

                # click lastpass extension       
                pyautogui.click(x=1416, y=63)

                # Wait for lastpass vault button image to appear
                image_vault = None
                while image_vault is None:
                    image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

                # lastpass search ven and click 
                # delay 0.5second
                page2.wait_for_timeout(500)
                pyautogui.write(ven_id)
                # delay 0.5second
                page2.wait_for_timeout(500)
                # Mouse Click
                pyautogui.click(x=1260, y=170)
                # delay 0.5second
                page2.wait_for_timeout(500)

                # Click "下一步" 
                __class__.red_Check(page2.locator("//button[@type='button']"), "Wait '下一步'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//button[@type='button']"), "OK! Click 下一步")
                page2.locator('//button[@type="button"]').click()
                
                # Wait for "*用户密码" appear
                __class__.red_Check(page2.locator("//label[contains(text(),'用户密码')]"), "Wait '*用户密码'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//label[contains(text(),'用户密码')]"), "OK!")

                # delay 0.3second
                page2.wait_for_timeout(300)

                # Click “登入”
                __class__.red_Check(page2.locator("//button[@type='submit']"), "Wait '*用户密码'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//button[@type='submit']"), "OK!")
                page2.locator('//button[@type="submit"]').click()
                
                # delay 0.3second
                page2.wait_for_timeout(300)

                # Wait for "验证安全邮箱" appear
                __class__.red_Check(page2.locator("//h3[contains(text(),'验证安全邮箱')]"), "Wait '验证安全邮箱'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//h3[contains(text(),'验证安全邮箱')]"), "OK!")

                # Click "获取验证码" 
                __class__.red_Check(page2.locator("//span[contains(text(),'获取验证码')]"), "Wait '验证安全邮箱'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//span[contains(text(),'获取验证码')]"), "OK!")
                page2.locator('//span[contains(text(),"获取验证码")]').click()

                # Switch to Gmail
                page.bring_to_front()  

                # 等待gmail alibaba验证码 跳出
                try:
                    while True:
                        try:
                            # Wait until at least one unread email is visible
                            page.wait_for_selector("tr.zE:has-text('Alibaba Cloud'):has-text('Security Verification Code'):has-text('- This email is sent by Alibaba Cloud and is automatically generated. Please do not reply directly. ')", timeout=5000)
                            break
                        except:
                            # Mail Refresh
                            page.locator('//div[@aria-label="Refresh"]//div[@class="asa"]').click()
                            continue
                    
                    # Check first 5 unread email rows
                    for i in range(5):
                        try:
                            row = page.locator("tr.zE").nth(i)
                            content = row.inner_text(timeout=3000)

                            if ("Alibaba Cloud" in content and 
                                "Security Verification Code" in content and 
                                "This email is sent by Alibaba Cloud" in content):
                                row.click()
                                break
                        except Exception as e:
                            continue  # Skip if row not available or timeout

                except TimeoutError:
                    print("No unread Alibaba Cloud email appeared in time.")

                # wait for ""1.  This code is required to complete your account verification or secure login process.""
                page.locator("//p[contains(text(),'1.  This code is required to complete your account')]").wait_for(timeout=0)

                # Regex to remove the unnecessary text, and keep only verification code
                v_code = page.locator("//tbody//tr//p[2]").text_content()
                v_code = re.search(r"Your verification code is:\s*(\d+)", v_code)
                v_code = v_code.group(1)

                # remove whitespace
                v_code = v_code.strip()
                print(f"Alibaba Verification Code: {v_code}")

                # delay 1second
                page.wait_for_timeout(1000)  

                # Click gmail “inbox”
                page.locator('(//div[@class="aio UKr6le"])[1]').click()
                
                # Switch to alibaba tab
                page2.bring_to_front()  

                # delay 1second
                page2.wait_for_timeout(1000) 

                # Wait for "验证安全邮箱" to be appear
                __class__.red_Check(page2.locator("//h3[contains(text(),'验证安全邮箱')]"), "Wait ‘验证安全邮箱'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//h3[contains(text(),'验证安全邮箱')]"), "OK!")

                # Click "x mark"
                page2.locator('//i[@class="next-icon next-icon-close next-xs"]').click()
                
                # Fill Verification Code
                page2.fill("//input[@id='EMAIL_CODE']", v_code)

                # delay 0.5second
                page2.wait_for_timeout(500) 

                # Click "提交验证码"
                page2.locator('//button[@type="submit"]').click()

                # Wait for "本月消费概览" appear
                __class__.red_Check(page2.locator("//span[contains(text(),'本月消费概览')]"), "Wait ‘本月消费概览'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//span[contains(text(),'本月消费概览')]"), "OK!")

                # Mouse Click
                pyautogui.click(x=1100, y=287)

                # Wait for "VISA" to be appear
                __class__.red_Check(page2.locator("//span[@class='payment-cardrand-visa']"), "Wait ‘VISA LOGO'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//span[@class='payment-cardrand-visa']"), "OK!")

                # Check if overdue payment
                try:
                    overdue = page2.locator("//p[@ng-repeat='item in vm.topTipsArr']").wait_for(timeout=2000)
                    __class__.red_Check(page2.locator("//p[@ng-repeat='item in vm.topTipsArr']"), "欠费 欠费 欠费 欠费 欠费 欠费'")
                    __class__.green_Check(page2.locator("//p[@ng-repeat='item in vm.topTipsArr']"), "欠费 欠费 欠费 欠费 欠费 欠费'")
                    print(f"{ven_id}= ", overdue)   
                except:
                    pass

                # Screenshot
                ImageGrab.grab().save(f'./watermelon/{ven_id}.png')
                
                # Wait for "RAM 用户" to be appear
                __class__.red_Check(page2.locator("//div[@class='sc-taltu8-3 CB-cquEbr']"), "Wait 'RAM 用户'")
                page2.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//div[@class='sc-taltu8-3 CB-cquEbr']"), "OK!")

                # delay 0.3second
                page2.wait_for_timeout(300)

                # hover to menu
                __class__.red_Check(page2.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!")
                __class__.green_Check(page2.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!")
                page2.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # if hover menu doesnt appear, rehover again
                while True:
                    try:
                        # Wait for "安全管控" to be appear
                        expect(page2.locator("//span[contains(text(),'安全管控')]")).to_be_visible(timeout = 1000) 
                        __class__.red_Check(page2.locator("//span[contains(text(),'安全管控')]"), "Wait '安全管控'")
                        page.wait_for_timeout(300)
                        __class__.green_Check(page2.locator("//span[contains(text(),'安全管控')]"), "OK!")
                        break
                    except:
                        # Mouse Click
                        pyautogui.click(x=1100, y=287)
                        # delay 0.5second
                        page.wait_for_timeout(500)
                        # hover to menu
                        __class__.red_Check(page2.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Wait 'Hover Menu'")
                        __class__.green_Check(page2.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover Menu")
                        page2.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # Wait for "安全管控" to be appear
                __class__.red_Check(page2.locator("//span[contains(text(),'安全管控')]"), "Wait '安全管控'")
                page.wait_for_timeout(300)
                __class__.green_Check(page2.locator("//span[contains(text(),'安全管控')]"), "OK!")

                # delay 0.5second
                page2.wait_for_timeout(500)

                # Click "退出登录" Logout
                __class__.red_Check(page2.locator("//a[contains(text(),'退出登录')]"), "Wait '退出登录'")
                __class__.green_Check(page2.locator("//a[contains(text(),'退出登录')]"), "退出登录")
                page2.locator("//a[contains(text(),'退出登录')]").click(force=True)

                # delay 0.5second
                page2.wait_for_timeout(500)

# Tencent Automation
class Tencent(Automation):

    # 腾讯云【中国站】
    @classmethod
    def tencent_CN(cls):
        with sync_playwright() as p:  
            
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            page.goto("https://cloud.tencent.com/login?s_url=https://console.cloud.tencent.com/expense/overview", wait_until="domcontentloaded")

            # if is "子用户登录" then click "切换登录方式", else skip
            try:
                expect(page.locator("//h3[contains(text(),'子用户登录')]")).to_be_visible(timeout= 2000) # "登录验证"
                # Click "切换登录方式"
                page.locator("//button[@class='accsys-control-panel__header-back']").click()
            except:
                pass
  
            # wait for "邮箱登录" to be appear
            page.locator("//div[contains(text(),'邮箱登录')]").wait_for(timeout=0) 

            # Click "邮箱登录" to Login
            page.locator("//div[contains(text(),'邮箱登录')]").click()

            # click lastpass extension       
            pyautogui.click(x=1416, y=63)

            # Wait for lastpass vault button image to appear
            image_vault = None
            while image_vault is None:
                image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

            # lastpass search ven and click 
            # delay 0.5second
            page.wait_for_timeout(500)
            pyautogui.write("ven182")
            # delay 0.5second
            page.wait_for_timeout(500)
            # Mouse Click
            pyautogui.click(x=1260, y=170)
            # delay 0.5second
            page.wait_for_timeout(500)

            # Click "登录" to Login
            page.locator("//span[@class='accsys-tp-btn__text'][contains(text(),'登录')]").click()
            # Move mouse to aside, prevent chatgpt cannot see the image clearly
            pyautogui.click(x=395, y=309)

            # wait for CAPTCHA "image验证" to be appear
            loop_count = 0
            while True:
                loop_count += 1
                print(f"🔁 Wait for 验证跳出 or 可用余额... #{loop_count}")

                try:
                    # set iframe
                    iframe = page.frame_locator("//iframe[@id='tcaptcha_iframe_dy']")

                    # Check whether Captcha is present
                    try:
                        title = iframe.locator("//span[@id='pHeaderTitle']").text_content(timeout=1000)
                    except:
                        title = None

                    # if title contains "选择" or "图片", then it is a captcha challenge
                    if title and "选择" in title and "图片" in title:
                        print(f"🛑 Captcha challenge detected: {title}")

                        # Chatgpt solve captcha...
                        page.wait_for_timeout(2000)
                        screenshot = pyautogui.screenshot(region=(619, 296, 360, 359))
                        screenshot.save('./晚班水位/ven182.png')

                        gpt_client = MyChatGPT()
                        prompt = "请根据截图中的提示，指出要点击的格子，例如 '1-2, 2-3'"
                        response_text = gpt_client.ask_gpt_about_image('./晚班水位/ven182.png', prompt)
                        print("🧠 GPT Response:", response_text)

                        gpt_client.extract_positions_and_click(response_text)
                        iframe.locator("//button[@id='verifyBtn']").click()

                        # Mouse mouse to prevent it block the screenshot, causing chatgpt unable to solve captcha
                        pyautogui.click(x=395, y=309)
                        page.wait_for_timeout(3000)

                        # Check again x times
                        continue

                except Exception as e:
                    print(f"[Debug] No captcha detected this loop: {e}")

                # 检查可用余额
                try:
                    page.locator("//h3[contains(text(),'可用余额')]").wait_for(timeout=2000)
                    print("✅ 可用余额 appeared. Captcha solved.")
                    break
                except:
                    pass
            
            # Wait for element == "a value/text"
            expect(page.locator("//div[@class='tc-g account-summary-data']//div[3]//div[2]")).to_have_text("0.00 元", timeout=5000)

            # delay 0.5second
            page.wait_for_timeout(500)

            # Extract Credit
            credit = page.locator(f"//div[@id='available-amount']").text_content()

            # Replace
            credit = credit.replace(',', '')
            credit = credit.replace('元', '')

            # MongoDB Update Data
            mangos_id = {'_id': ObjectId(tencent_CN_MONGODB[m_id])}
            collection.update_one(mangos_id, {"$set": {"Credit": credit}})
            print(f"ven182= {credit}")
            # mongdb+id +1
            m_id += 1

            # delay 0.5second
            page.wait_for_timeout(500)

            # hover to menu
            pyautogui.moveTo(1502, 105)

            # wait for "安全设置" to be appear
            page.locator("//span[contains(text(),'安全设置')]").wait_for(state="visible", timeout=0)

            # delay 0.5second
            page.wait_for_timeout(500)

            # Screenshot
            ImageGrab.grab().save('./晚班水位/ven182.png')

            # delay 0.5second
            page.wait_for_timeout(500)

            # Click "logout" to Login
            page.locator("//button[contains(text(),'退出')]").click()

            # delay 3second
            page.wait_for_timeout(3000)

    # 腾讯云【中国站】 子用户登录
    @classmethod
    def tencent_CN_SUB(cls):
        with sync_playwright() as p:  
            
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            page.goto("https://cloud.tencent.com/login/subAccount?s_url=https%3A%2F%2Fconsole.cloud.tencent.com%2Fexpense%2Foverview", wait_until="domcontentloaded")

            # wait for "子用户登录" to be appear
            page.locator("//h3[contains(text(),'子用户登录')]").wait_for(timeout=0) 

            # click lastpass extension       
            pyautogui.click(x=1416, y=63)

            # Wait for lastpass vault button image to appear
            image_vault = None
            while image_vault is None:
                image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

            # lastpass search ven and click 
            # delay 0.5second
            page.wait_for_timeout(500)
            pyautogui.write("ven322")
            # delay 0.5second
            page.wait_for_timeout(500)
            # Mouse Click
            pyautogui.click(x=1260, y=170)
            # delay 0.5second
            page.wait_for_timeout(500)

            # Click "登录" to Login
            page.locator("//button[@type='submit']//span[@class='accsys-tp-btn__text'][contains(text(),'登录')]").click()

            # delay 0.5second
            page.wait_for_timeout(500)
        
            # wait for "可用余额" to be appear
            page.locator("//h3[contains(text(),'可用余额')]").wait_for(timeout=0) 

            # Wait for element == "a value/text"
            expect(page.locator("//div[@class='tc-g account-summary-data']//div[3]//div[2]")).to_have_text("0.00 元", timeout=5000)

            # delay 0.5second
            page.wait_for_timeout(500)

            # Extract Credit
            credit = page.locator(f"//div[@id='available-amount']").text_content()

            # Replace
            credit = credit.replace(',', '')
            credit = credit.replace('元', '')

            # MongoDB Update Data
            mangos_id = {'_id': ObjectId(tencent_CN_SUB_MONGODB[m_id])}
            collection.update_one(mangos_id, {"$set": {"Credit": credit}})
            print(f"ven322= {credit}")
            # mongdb+id +1
            m_id += 1

            # wait for "子用户" to be appear
            page.locator("(//p[@class='sdk-nav-v2-nav-user-info-account-text'])[1]").wait_for(timeout=0) 

            # hover to menu
            pyautogui.moveTo(1492, 112)

            # wait for "安全设置" to be appear
            page.locator("//span[contains(text(),'安全设置')]").wait_for(timeout=0) 

            # delay 0.5second
            page.wait_for_timeout(500)

            # Screenshot
            ImageGrab.grab().save('./晚班水位/ven322.png')

            # delay 0.5second
            page.wait_for_timeout(500)

            # Click "logout" to Login
            page.locator("//button[contains(text(),'退出')]").click()

            # delay 2second
            page.wait_for_timeout(2000)

    # 腾讯云【国际站】
    @classmethod
    def tencent_INT(cls):
        with sync_playwright() as p:  
            
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            page.goto("https://www.tencentcloud.com/zh/account/login?s_url=https://console.tencentcloud.com/expense/rmc/accountinfo", wait_until="domcontentloaded")

            # if is "子用户登录" then click "切换登录方式", else skip
            try:
                if page.locator("text='CAM用户登录'").is_visible(timeout=2000):
                    # Click "主账号登录"
                    page.locator("//a[contains(text(),'主账号登录')]").click()
            except:
                pass

            for ven_id in tencent_INT_ID:

                # wait for "邮箱登录" to be appear
                page.locator("//div[@class='LoginCommonBox_clg-mod-title__gpSTl tcas-login-panel__box-title']").wait_for(timeout=0) 

                # delay 0.5second
                page.wait_for_timeout(500)

                # click lastpass extension       
                pyautogui.click(x=1416, y=63)

                # Wait for lastpass vault button image to appear
                image_vault = None
                while image_vault is None:
                    image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

                # lastpass search ven and click 
                # delay 0.5second
                page.wait_for_timeout(500)
                pyautogui.write(ven_id)
                # delay 0.5second
                page.wait_for_timeout(500)
                # Mouse Click
                pyautogui.click(x=1260, y=170)
                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "登录" to Login
                page.locator("//button[@type='submit']//span[contains(text(),'登录')]").click()

                # wait for "账户信息" to be appear
                page.locator("//h2[contains(text(),'账户信息')]").wait_for(timeout=0) 
                # wait for "可用额度" to be appear
                page.locator("//h3[contains(text(),'可用额度')]").wait_for(timeout=0) 

                # delay 1second
                page.wait_for_timeout(1000)

                # Extract Credit
                credit = page.locator(f"(//div[@class='data-value arrows'])[1]").text_content()

                # Replace
                credit = credit.replace(',', '')
                credit = re.sub(r'USD.*', 'USD', credit)
                credit = credit.replace('USD', '')

                # Remove Whitespace
                credit = credit.strip()

                # MongoDB Update Data
                mangos_id = {'_id': ObjectId(tencent_INT_MONGODB[m_id])}
                collection.update_one(mangos_id, {"$set": {"Credit": credit}})
                print(f"{ven_id}= {credit}")
                # mongdb+id +1
                m_id += 1

                # hover to menu
                pyautogui.moveTo(1551, 110)

                # wait for "安全设置" to be appear
                page.locator("//a[contains(text(),'安全设置')]").wait_for(timeout=0) 

                # delay 0.5second
                page.wait_for_timeout(500)

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "logout" to Login
                page.locator("//a[contains(text(),'退出')]").click()

                # delay 1second
                page.wait_for_timeout(1000)
            
    # 腾讯云【国际站】CAM用户登录
    @classmethod
    def tencent_INT_CAM(cls):
        with sync_playwright() as p:  
            
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            
            for ven_id in tencent_CAM_ID:

                page.goto(Tencent_Webpage[m_id], wait_until="domcontentloaded")

                # wait for "CAM用户登录" to be appear
                page.locator("//div[@class='LoginCommonBox_clg-mod-title__gpSTl tcas-login-panel__box-title']").wait_for(timeout=0) 

                # delay 0.5second
                page.wait_for_timeout(500)

                # click lastpass extension       
                pyautogui.click(x=1416, y=63)

                # Wait for lastpass vault button image to appear
                image_vault = None
                while image_vault is None:
                    image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

                # lastpass search ven and click 
                # delay 0.5second
                page.wait_for_timeout(500)
                pyautogui.write(ven_id)
                # delay 0.5second
                page.wait_for_timeout(500)
                # Mouse Click
                pyautogui.click(x=1260, y=170)
                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "登录" to Login
                page.locator("//button[@type='submit']").click()

                # wait for "账户信息" to be appear
                page.locator("//h2[contains(text(),'账户信息')]").wait_for(timeout=0) 
                # wait for "可用额度" to be appear
                page.locator("//h3[contains(text(),'可用额度')]").wait_for(timeout=0) 

                # delay 1second
                page.wait_for_timeout(1000)

                # Extract Credit
                credit = page.locator("(//div[@class='data-value arrows'])[1]").text_content()

                # Replace
                credit = credit.replace(',', '')
                credit = re.sub(r'USD.*', 'USD', credit)
                credit = credit.replace('USD', '')

                # Remove Whitespace
                credit = credit.strip()

                # MongoDB Update Data
                mangos_id = {'_id': ObjectId(tencent_INT_CAM_MONGODB[m_id])}
                collection.update_one(mangos_id, {"$set": {"Credit": credit}})
                print(f"{ven_id}= {credit}")
                # mongdb+id +1
                m_id += 1

                # hover to menu
                pyautogui.moveTo(1551, 110)

                # wait for "安全设置" to be appear
                page.locator("//a[contains(text(),'安全设置')]").wait_for(timeout=0) 

                # delay 0.5second
                page.wait_for_timeout(500)

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "logout" to Login
                page.locator("//a[contains(text(),'退出')]").click()

                # delay 1second
                page.wait_for_timeout(1000)
    
    # 腾讯云【国际站】ven295 (Tencent Website Bug)
    @classmethod
    def tencent_ven295(cls):
        with sync_playwright() as p:  
                    
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            page.goto("https://intl.cloud.tencent.com/zh/account/login?s_url=https%3A%2F%2Fconsole.intl.cloud.tencent.com%2Fexpense%2Frmc%2Faccountinfo", wait_until="domcontentloaded")

            # wait for "邮箱登录" to be appear
            page.locator("//div[@class='LoginCommonBox_clg-mod-title__gpSTl tcas-login-panel__box-title']").wait_for(timeout=0) 
            
            # delay 0.5second
            page.wait_for_timeout(500)

            # click lastpass extension       
            pyautogui.click(x=1416, y=63)

            # Wait for lastpass vault button image to appear
            image_vault = None
            while image_vault is None:
                image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

            # lastpass search ven and click 
            # delay 0.5second
            page.wait_for_timeout(500)
            pyautogui.write("ven295")
            # delay 0.5second
            page.wait_for_timeout(500)
            # Mouse Click
            pyautogui.click(x=1260, y=170)
            # delay 0.5second
            page.wait_for_timeout(500)

            # Click "submit" to Login
            page.locator("//button[@type='submit']").click()

            # wait for "可用额度" to be appear
            page.locator("//h3[contains(text(),'可用额度')]").wait_for(timeout=0) 

            # wait for "0 张 （7日内到期0张）" to be appear
            page.locator(":has-text('0 张 （7日内到期0张）')")

            # delay 1.5second
            page.wait_for_timeout(1500)

            # Extract Credit
            credit = page.locator("(//div[@class='data-value arrows'])[1]").text_content()

            # Replace
            credit = credit.replace(',', '')
            credit = re.sub(r'USD.*', 'USD', credit)
            credit = credit.replace('USD', '')

            # Remove Whitespace
            credit = credit.strip()

            # MongoDB Update Data
            mangos_id = {'_id': ObjectId(tencent_INT_ven295_MONGODB[m_id])}
            collection.update_one(mangos_id, {"$set": {"Credit": credit}})
            print(f"ven295 = {credit}")
            # mongdb+id +1
            m_id += 1

            # hover to menu
            page.locator("//a[@class='fn-sdk-nav-dropdown-item sdk-nav-account']").hover()

            # wait for "安全设置" to be appear
            page.locator("//a[contains(text(),'安全设置')]").wait_for(timeout=0) 

            # Screenshot
            ImageGrab.grab().save('./晚班水位/ven295.png')

            # delay 0.5second
            page.wait_for_timeout(500)

            # Click "logout" to Login
            page.locator("//a[contains(text(),'退出')]").click()

            # delay 1second
            page.wait_for_timeout(1000)

# Huawei Automation
class Huawei(Automation):
    
    # Huawei OPSADMIN
    @classmethod
    def huawei_OPSADMIN(cls):
        with sync_playwright() as p:  
            
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            
            for ven_id in huawei_OPSADMIN_ID:

                # Huawei OPSADMIN Login
                page.goto(Huawei_Webpage[m_id], timeout=15000, wait_until="domcontentloaded")

                # wait for "IAM用户登录" to be appear
                page.locator("//span[@class='loginTypeNoSelected ng-binding']").wait_for(timeout=0) 

                # delay 0.5second
                page.wait_for_timeout(500)

                # click lastpass extension       
                pyautogui.click(x=1416, y=63)

                # Wait for lastpass vault button image to appear
                image_vault = None
                while image_vault is None:
                    image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

                # lastpass search ven and click 
                # delay 0.5second
                page.wait_for_timeout(500)
                pyautogui.write(ven_id)
                # delay 0.5second
                page.wait_for_timeout(500)
                # Mouse Click
                pyautogui.click(x=1260, y=170)
                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "登录" to Login
                page.locator("//span[@id='btn_submit']").click()

                # Check Verification Whether is Appear or not
                if ven_id == "ven399":
                    # ven399 MFA Verfication Appear
                    # wait for 上次登录成功时间 appear
                    expect(page.locator("//div[contains(text(),'上次登录成功时间')]")).to_be_visible(timeout= 0) # "登录验证"

                    # delay 1second
                    page.wait_for_timeout(1000)

                    # Click "登录" to Login
                    page.locator("//div[@id='submitBtn']").click()
                else:
                    # MFA Verification Appear, if appear do something... else skip...
                    # if "登录验证" appear within a 3 seconds then continue.... else skip
                    try:
                        # wait for "登录验证" to be appear
                        expect(page.locator("//p[@class='ng-binding']")).to_have_text("登录验证", timeout=3000)

                        # mark checkbox
                        page.check("//input[@id='promptBindAndEnableCheckbox']")

                        # Button click 暂不绑定
                        page.locator("xpath=//div[@id='promptBindAndEnableCancelBtn']").click(force=True)  
                    except:
                        pass

                # wait for "Intl-简体" to be appear
                page.locator("//span[contains(text(),'Intl-简体')]").wait_for(timeout=0) 

                # delay 1.5second
                page.wait_for_timeout(1500)

                # Go to “费用”
                page.goto("https://account-intl.huaweicloud.com/usercenter/?region=ap-southeast-1&locale=zh-cn#/userindex/allview", wait_until="domcontentloaded")
                
                # wait for "本月剩余预算" to be appear
                page.locator("//span[contains(text(),'本月剩余预算')]").wait_for(timeout=0) 

                # wait for "//div[@id='status-message']" element appear this text "0 个"
                expect(page.locator("//div[@class='part text-left']")).to_have_text("0 个", timeout=0)

                # delay 0.5second
                page.wait_for_timeout(500)

                # Extract Credit
                credit = page.locator("//span[@id='remainAmount_bindtype3']").text_content()

                # Replace
                credit = credit.replace(',', '')
                credit = credit.replace('$', '')
                credit = credit.replace(' USD', '')

                # Remove Whitespace
                credit = credit.strip()

                # MongoDB Update Data
                mangos_id = {'_id': ObjectId(huawei_OPSADMIN_MONGODB[m_id])}
                collection.update_one(mangos_id, {"$set": {"Credit": credit}})
                print(f"{ven_id}= {credit}")
                # mongdb+id +1
                m_id += 1

                # hover to menu
                pyautogui.moveTo(1502, 105)

                # wait for "安全设置" to be appear
                page.locator("//a[@id='cf_user_info_securitySettings_common']").wait_for(timeout=0) 

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "logout" to Login
                page.locator("//span[@id='cf_user_info_logout']").click()

                # delay 2second
                page.wait_for_timeout(2000)

                # wait for "IAM用户登录" to be appear
                page.locator("//span[contains(text(),'华为账号登录')]").wait_for(timeout=0) 

    # Huawei
    @classmethod
    def huawei(cls):
        with sync_playwright() as p:  
            
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            page.goto("https://auth.huaweicloud.com/authui/login.html?service=https://account-intl.huaweicloud.com/usercenter/#/login", wait_until="domcontentloaded")
            
            for ven_id in huawei_ID:

                # wait for "华为账号登录" to be appear
                page.locator("//span[contains(text(),'华为账号登录')]").wait_for(timeout=0) 

                # delay 0.5second
                page.wait_for_timeout(500)

                # click lastpass extension       
                pyautogui.click(x=1416, y=63)

                # Wait for lastpass vault button image to appear
                image_vault = None
                while image_vault is None:
                    image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

                # lastpass search ven and click 
                # delay 0.5second
                page.wait_for_timeout(500)
                pyautogui.write(ven_id)
                # delay 0.5second
                page.wait_for_timeout(500)
                # Mouse Click
                pyautogui.click(x=1260, y=170)
                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "登录" to Login
                page.locator("//div[@class='hwid-btn hwid-btn-primary']").click()

                # MFA Verification Appear, if appear do something... else skip...
                try:
                    # wait for "MFA设备类型" appear
                    expect(page.locator("//div[@class='device-type ng-binding']")).to_be_visible(timeout= 2000) # 

                    # mark checkbox
                    page.check("//input[@id='promptBindAndEnableCheckbox']")

                    # Button click 暂不绑定
                    page.locator("xpath=//div[@id='promptBindAndEnableCancelBtn']").click(force=True)  
                except:
                    pass

                # wait for "本月剩余预算" to be appear
                page.locator("//span[contains(text(),'本月剩余预算')]").wait_for(timeout=0) 

                # wait for "//div[@id='status-message']" element appear this text "0 个"
                page.locator(":has-text('0 个'):has-text('1 个')")
                
                # delay 0.5second
                page.wait_for_timeout(500)

                # Extract Credit
                credit = page.locator("//span[@id='remainAmount_bindtype3']").text_content()

                # Replace
                credit = credit.replace(',', '')
                credit = credit.replace('$', '')
                credit = credit.replace(' USD', '')

                # Remove Whitespace
                credit = credit.strip()

                # MongoDB Update Data
                mangos_id = {'_id': ObjectId(huawei_MONGODB[m_id])}
                collection.update_one(mangos_id, {"$set": {"Credit": credit}})
                print(f"{ven_id}= {credit}")
                # mongdb+id +1
                m_id += 1

                # hover to menu
                pyautogui.moveTo(1502, 105)

                # wait for "安全设置" to be appear
                page.locator("//a[@id='cf_user_info_securitySettings_common']").wait_for(timeout=0) 

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "logout" to Login
                page.locator("//span[@id='cf_user_info_logout']").click()

                # delay 1second
                page.wait_for_timeout(1000)

# Ucloud Automation
class Ucloud(Automation):

    # Ucloud
    @classmethod
    def ucloud(cls):
        with sync_playwright() as p:  
                
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            page.goto("https://passport.ucloud.cn/#login", wait_until="domcontentloaded")
            
            # wait for "账号登录" to be appear
            page.locator("//div[@class='social-title-left']").wait_for(timeout=0) 

            # delay 0.5second
            page.wait_for_timeout(500)

            # click lastpass extension       
            pyautogui.click(x=1416, y=63)

            # Wait for lastpass vault button image to appear
            image_vault = None
            while image_vault is None:
                image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

            # lastpass search ven and click 
            # delay 0.5second
            page.wait_for_timeout(500)
            pyautogui.write("ven281")
            # delay 0.5second
            page.wait_for_timeout(500)
            # Mouse Click
            pyautogui.click(x=1260, y=170)
            # delay 1second
            page.wait_for_timeout(1000)

            # Click "登录" to Login
            page.locator("(//button[contains(text(),'登录')])[1]").click()

            # wait for "私有网络" to be appear
            page.locator("//h2[contains(text(),'私有网络')]").wait_for(timeout=0) 

            # delay 0.5second
            page.wait_for_timeout(500)

            # Click Logout menu
            page.locator("//img[@class='header-user-icon']").click()

            # wait for "账户余额" to be appear
            page.locator("//div[contains(text(),'账户余额')]").wait_for(timeout=0) 

            # delay 1second
            page.wait_for_timeout(1000)

            # Extract Credit
            credit = page.locator("//span[@class='balance']").text_content()

            # Replace
            credit = credit.replace(',', '')

            # Remove Whitespace
            credit = credit.strip()

            # MongoDB Update Data
            mangos_id = {'_id': ObjectId(ucloud_MONGODB[m_id])}
            collection.update_one(mangos_id, {"$set": {"Credit": credit}})
            print(f"ven281 = {credit}")
            # mongdb+id +1
            m_id += 1

            # Screenshot
            ImageGrab.grab().save('./晚班水位/ven281.png')

            # Click "logout" to Login
            page.locator("//span[contains(text(),'退出账号')]").click()

            # delay 1second
            page.wait_for_timeout(1000)

# Other Automation
class Other_Cloud(Automation): 
    
    # Gname
    @classmethod
    def gname(cls):
        with sync_playwright() as p:  
                    
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            page.goto("https://www.gname.com/login?refer=https%3A%2F%2Fwww.gname.com%2Fuser", wait_until="domcontentloaded")
        
            for ven_id in gname_ID:

                # if is in english page, switch to chinese version
                try:
                    # wait for "Please enter your email" to be appear
                    page.locator("//input[@placeholder='Please enter your email']").wait_for(timeout=1000)   
                    # wait for ""Please enter the captcha"" to be appear
                    page.locator("//input[@placeholder='Please enter the captcha']").wait_for(timeout=1000)   

                    # hover to change language bar
                    page.locator("//span[@class='langx']").hover()
                    
                    # delay 0.5second
                    page.wait_for_timeout(500)

                    # Click "中文版" switch to login
                    page.locator("//li[contains(text(),'中文版')]").click()      

                    # delay 0.5second
                    page.wait_for_timeout(500)
                except:
                    pass

                # wait for "邮箱登录" to be appear
                page.locator("//span[@class='login-nav-btn']").wait_for(timeout=0)  

                # Click "密码登录"
                page.locator("//html/body/div[2]/div/div[2]/div[2]/div/div[1]/span[2]").click() 

                # delay 0.5second
                page.wait_for_timeout(500)

                # click lastpass extension       
                pyautogui.click(x=1416, y=63)

                # Wait for lastpass vault button image to appear
                image_vault = None
                while image_vault is None:
                    image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

                # lastpass search ven and click 
                # delay 0.5second
                page.wait_for_timeout(500)
                pyautogui.write(ven_id)
                # delay 0.5second
                page.wait_for_timeout(500)
                # Mouse Click
                pyautogui.click(x=1260, y=170)
                # delay 1second
                page.wait_for_timeout(1000)

                # Drag & Drop 登入
                pyautogui.moveTo(872, 518, 0.4)
                pyautogui.dragTo(1266, 507, button='left', duration=0.4)

                # wait for "Gname 一对一高效服务" to be appear
                try:
                    page.locator("//h3[contains(text(),'Gname 一对一高效服务')]").wait_for(timeout=1500) 

                    # delay 0.5second
                    page.wait_for_timeout(500)

                    # Mouse Click "X"
                    pyautogui.click(x=1001, y=342)
                except:
                    pass

                # if is in english page, switch to chinese version
                try:
                    # wait for "Please enter your email" to be appear
                    page.locator("//strong[normalize-space()='English']").wait_for(timeout=1500)   

                    # hover to change language bar
                    page.locator("//span[@class='switch-zw']").hover()
                    
                    # delay 0.5second
                    page.wait_for_timeout(500)

                    # Click "中文版" switch to login
                    page.locator("//span[@lang='zhcn']").click()         

                    # delay 0.5second
                    page.wait_for_timeout(500)
                except:
                    pass

                # wait for "资金信息" to be appear
                page.locator("//span[contains(text(),'资金信息')]").wait_for(timeout=0) 

                # delay 0.5second
                page.wait_for_timeout(500)

                # Extract Credit
                credit = page.locator("//div[@class='kyye zjxx-item']").text_content()

                # Regex
                credit = re.search(r"\d+\.\d+", credit)
                credit = credit.group(0)

                # Remove Whitespace
                credit = credit.strip()

                # MongoDB Update Data
                mangos_id = {'_id': ObjectId(gname_MONGODB[m_id])}
                collection.update_one(mangos_id, {"$set": {"Credit": credit}})
                print(f"{ven_id}= {credit}")
                # mongdb+id +1
                m_id += 1

                # hover to menu
                # pyautogui.moveTo(1535, 160)
                page.locator("//a[@class='user-rank']").hover()

                # wait for "退出" to be appear
                page.locator("//a[@id='logout']").wait_for(timeout=0) 

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # delay 1second
                page.wait_for_timeout(1000)

                # Click "logout" to Logout
                page.locator("//a[@id='logout']").click()

                # delay 0.5second
                page.wait_for_timeout(500)

    # SMS-MAN
    @classmethod
    def sms_man(cls):
        with sync_playwright() as p:  

            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            page.goto("https://sms-man.com/", wait_until="domcontentloaded")

            try:
                # wait for "Sign Up" to be appear
                page.locator("//*[@id='header__btns']/a[1]/span").wait_for(timeout=5000) 

                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "Log In" 
                page.locator("//*[@id='header__btns']/a[2]/span").click() 

                # wait for "Log In" to be appear
                page.locator("//*[@id='vapp']/main/section/div[2]/div[1]/div[1]/span").wait_for(timeout=0) 

                # delay 0.5second
                page.wait_for_timeout(500)

                # Wait for Cloudflare verification pass
                cloudflare_pass = None
                while cloudflare_pass is None:
                    cloudflare_pass = pyautogui.locateOnScreen('./image/cloudflare_pass.png', grayscale = True)

                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "Login" 
                page.locator("//*[@id='vapp']/main/section/div[2]/div[1]/form/button/span").click() 

            except:
                pass

            # Wait for 1. Select a service image appear
            select_Service_img = None
            while select_Service_img is None:
                select_Service_img = pyautogui.locateOnScreen('./image/select_service.png', grayscale = True)

            # delay 0.5second
            page.wait_for_timeout(500)

            # Extract Credit
            credit = page.locator("input.user-payment__input").get_attribute("value")

            # Replace
            credit = credit.replace('$', '')
            credit = credit.replace('\n', '')
            
            # MongoDB Update Data
            mangos_id = {'_id': ObjectId(sms_MONGODB[m_id])}
            collection.update_one(mangos_id, {"$set": {"Credit": credit}})
            print(f"ven326 = {credit}")
            # mongdb+id +1
            m_id += 1
            
            # Screenshot
            ImageGrab.grab().save('./晚班水位/ven326.png')
            
            # delay 0.5second
            page.wait_for_timeout(500)

    # 7211.com
    @classmethod
    def s211(cls):
        with sync_playwright() as p:  
                    
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            page.goto("https://www.7211.com/login.php", wait_until="domcontentloaded")

            # wait for "请先登录再下单" to be appear
            page.locator("//h2[contains(text(),'请先登录再下单！')]").wait_for(timeout=0) 

            # delay 0.5second
            page.wait_for_timeout(500)

            # Click "登录" to Login
            page.locator("//button[contains(text(),'登录')]").click()

            # wait for "购买一个" to be appear
            page.locator("//h2[contains(text(),'购买一个')]").wait_for(timeout=0) 

            # delay 0.5second
            page.wait_for_timeout(500)
            
            # hover to menu
            page.locator("//li[@class='user-opt']").hover()

            # delay 0.5second
            page.wait_for_timeout(500)

            # Click "我的账号" 
            page.locator("//a[contains(text(),'我的账号')]").click()

            # wait for "帐单概要" to be appear
            page.locator("//a[contains(text(),'帐单概要')]").wait_for(timeout=0) 

            # delay 0.5second
            page.wait_for_timeout(500)

            # Click "帐单概要" 
            page.locator("//a[contains(text(),'帐单概要')]").click()

            # wait for "资金概览" to be appear
            page.locator("//h1[contains(text(),'资金概览')]").wait_for(timeout=0) 

            # delay 0.5second
            page.wait_for_timeout(500)

            # Extract Credit
            credit = page.locator("//font[@color='red']").text_content()

            # Re
            credit = re.sub(r'CNY |\s+', '', credit)

            # Remove Whitespace
            credit = credit.strip()

            # MongoDB Update Data
            mangos_id = {'_id': ObjectId(S211_MONGODB[m_id])}
            collection.update_one(mangos_id, {"$set": {"Credit": credit}})
            print(f"ven196 = {credit}")
            # mongdb+id +1
            m_id += 1

            # Screenshot
            ImageGrab.grab().save('./晚班水位/ven196.png')

            # Click logout menu 
            page.locator("//a[@id='profile-image']").click()

            # delay 0.5second
            page.wait_for_timeout(500)

            # Click "退出“ logout 
            page.locator("//a[contains(text(),'退出')]").click()

            # delay 0.5second
            page.wait_for_timeout(500)

    # byteplus
    @classmethod
    def byteplus(cls):
        with sync_playwright() as p:  
                    
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            
            for ven_id in byteplus_ID:

                page.goto("https://console.byteplus.com/finance/overview", wait_until="domcontentloaded")

                # wait for "Sign in" to be appear
                page.locator("//div[@class='title-_WOXN_']").wait_for(timeout=0)

                # delay 0.5second
                page.wait_for_timeout(500) 

                # click lastpass extension       
                pyautogui.click(x=1416, y=63)

                # Wait for lastpass vault button image to appear
                image_vault = None
                while image_vault is None:
                    image_vault = pyautogui.locateOnScreen("./image/vault3.png", grayscale = True)

                # lastpass search ven and click 
                # delay 0.5second
                page.wait_for_timeout(500)
                pyautogui.write(ven_id)
                # delay 0.5second
                page.wait_for_timeout(500)
                # Mouse Click
                pyautogui.click(x=1260, y=170)
                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "Sign in" to Login
                page.locator("//button[@type='submit']").click()

                # wait for "账户总览" to be appear
                page.locator("//div[@class='mZis6']").wait_for(timeout=0) 

                # delay 0.5second
                page.wait_for_timeout(500)

                # Extract Credit
                credit = page.locator("//div[5]//div[1]//p[2]").text_content()

                # Re
                credit = re.sub(r'[^\d.]', '', credit)

                # Remove Whitespace
                credit = credit.strip()

                # MongoDB Update Data
                mangos_id = {'_id': ObjectId(byteplus_MONGODB[m_id])}
                collection.update_one(mangos_id, {"$set": {"Credit": credit}})
                print(f"{ven_id} = {credit}")
                # mongdb+id +1
                m_id += 1

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # Click logout menu 
                page.locator("//div[@class='index-module__user-avatar-item--2dVCE']").click()

                # wait for "费用中心" to be appear
                page.locator("//a[@class='index-module__item--13iOw']//div[contains(text(),'费用中心')]").wait_for(timeout=0)

                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "退出“ logout 
                page.locator("//button[@class='bp-nav-btn bp-nav-btn-secondary bp-nav-btn-size-default bp-nav-btn-shape-square index-module__btn--3XoR5']").click()

                # delay 5second
                page.wait_for_timeout(5000)

# Zentaowater & Noctoolwater Automation
class Zentao_Noctool(Automation):

    @classmethod
    def zentaowater(cls):
        with sync_playwright() as p:  

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            page.goto("https://zr-zentao2023.cccqx.com/zentao/execution-task-26.html", wait_until="domcontentloaded")

            # if is in Login PAGE, else skip
            try:
                # Wait if "loginPanel" to be appear else pass
                expect(page.locator("//div[@id='loginPanel']")).to_be_visible(timeout= 2000) 

                # click lastpass extension       
                pyautogui.click(x=1416, y=63)

                # Wait for image Appear
                image_vault = None
                while image_vault is None:
                    image_vault = pyautogui.locateOnScreen('./image/vault3.png', grayscale = True)
                print("Lastpass Image Vault Loaded") 

                # delay 0.5second
                page.wait_for_timeout(500)
                # Mouse Click
                pyautogui.click(1176,212)   
                # delay 0.5second
                page.wait_for_timeout(500)
                # Click "登入" 
                page.locator("//button[@id='submit']").click()
                # delay 0.5second
                page.wait_for_timeout(500)
            except:
                pass

            ## Get iframe
            iframe = page.frame_locator("//div[@id='apps']//iframe[@id='appIframe-project']")

            ## Wait for "晚班週期性業務(複製用)" to be appear
            iframe.locator("//*[@id='datatable-taskList']/div[2]/div[1]/div/table/tbody/tr[3]/td[2]/a").wait_for(timeout=0) 

            ## Click "edit" 
            iframe.locator("//*[@id='datatable-taskList']/div[2]/div[3]/div/table/tbody/tr[1]/td/a[4]").click()

            ## Wait for "晚班週期性業務(複製用)" to be appear
            iframe.locator("//*[@id='dataform']/div[2]/div[1]/div/div[1]/div[1]").wait_for(timeout=0) 

            ## Wait for "备注" to be appear
            iframe.locator("//div[contains(text(),'备注')]").wait_for(timeout=0) 
            
            # delay 0.5second
            page.wait_for_timeout(500)
            
            ## Click "X" 
            try:
                iframe.locator("//div[@id='pri_chosen']//abbr[@class='search-choice-close']").click(timeout=1000)
            except:
                # Mouse Click
                pyautogui.click(x=365, y=749)
                pass

            # delay 0.5second
            page.wait_for_timeout(500) 

            # Mouse Click
            pyautogui.click(x=365, y=749)

            # delay 0.5second
            page.wait_for_timeout(500)

            # keyboard Enter 8 times
            pyautogui.press('enter', presses = 8)

            # delay 0.5second
            page.wait_for_timeout(500)
            
            # Mouse Click
            pyautogui.click(x=349, y=652)

            # delay 0.5second
            page.wait_for_timeout(500)
            
            # For loop Mongodb ID and Ven_ID
            for cloud_db, cloud_id in zip(all_Cloud_MONGODB, all_Cloud_ID): 
                for mongodb_id, ven_id in zip(cloud_db, cloud_id):

                    # Search mongodb database object ID
                    mangodb_id = {'_id': ObjectId(mongodb_id)}
                    documents = collection.find_one(mangodb_id)
                    ven_machine_value = documents.get('Ven_Machine','N/A')
                    credit_value = documents.get('Credit', 'N/A') 
                    unit_value = documents.get('Unit', 'N/A')
                    merge = ven_machine_value + " " + credit_value + " " + unit_value
                    
                    # Merge name ven_machine, credit and unit   
                    pyperclip.copy(merge)
                    pyautogui.hotkey("command", "v")

                    # Create an instance of the NSPasteboard class
                    pasteboard = NSPasteboard.generalPasteboard()

                    # Read image data from the file
                    with open(f"./晚班水位/{ven_id}.png", 'rb') as file:
                        image_data = file.read()

                    # Copy the image data to the clipboard as a PNG
                    if image_data:
                        pasteboard.declareTypes_owner_([NSPasteboardTypePNG], None)
                        pasteboard.setData_forType_(image_data, NSPasteboardTypePNG)
                        print(f"{ven_id} Image copied to clipboard.")
                    
                    # Paste Image
                    pyautogui.keyDown('command')
                    pyautogui.press('v')
                    pyautogui.keyUp('command')

                    # Next Line
                    pyautogui.press('enter', presses = 2)
                    # delay 0.5
                    # 
                    # second
                    page.wait_for_timeout(500) 


            ## Click "保存" 
            iframe.locator("//button[@id='submit']").click()

            # delay 3seconds
            page.wait_for_timeout(3000)  

    @classmethod
    def noctoolwater(cls):
        with sync_playwright() as p:  
                    
            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Wait for Chrome CDP to be ready
            cls.wait_for_cdp_ready()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            page.goto("http://10.77.1.196/stocks/", wait_until="domcontentloaded")

            # Wait for "記錄列表" to be appear
            page.locator("//h3[contains(text(),'記錄列表')]").wait_for(timeout=0) 

            # delay 0.5second
            page.wait_for_timeout(500)

            for cloud_db, cloud_id in zip(all_Cloud_MONGODB, all_Cloud_ID): 
                for mongodb_id, ven_id, links in zip(cloud_db, cloud_id, n_webpage):

                    # Go to the webpage
                    page.goto(links, wait_until="domcontentloaded")

                    # delay 0.5second
                    page.wait_for_timeout(500)

                    # Wait for "記錄量趨勢圖" to be appear
                    page.locator("//h5[contains(text(),'記錄量趨勢圖')]").wait_for(timeout=0) 
                    
                    # Mouse Click
                    pyautogui.click(x=961, y=414)

                    # delay 0.5second
                    page.wait_for_timeout(500)

                    # Mouse scroll down
                    pyautogui.scroll(-100)

                    # Previous Credit / Data
                    pre_credit = page.locator("//tbody/tr[1]/td[2]").text_content()

                    # Search mongodb database object ID
                    mangodb_id = {'_id': ObjectId(mongodb_id)}
                    documents = collection.find_one(mangodb_id)
                    credit_value = documents.get('Credit', 'N/A') 

                    # Fill credit
                    page.fill('//input[@id="id_stocks"]', credit_value)
                    # page.keyboard.press("Enter")  

                    print(f"{ven_id}= Previous: {pre_credit}, Actual: {credit_value} \n") 

                    # delay 0.5second
                    page.wait_for_timeout(500)

    def low_water ():
        
        print("\n【低于安全水位】\n")
        collection = __class__.mongodb_atlas()
        documents = collection.find()

        for doc in documents:
            if float(doc.get("Credit", 0)) < float(doc.get("Secure_Credit", 0)):
                print(f"{doc.get('Ven_Machine')} 已低于安全流量 (当前存量：{doc.get('Credit')} {doc.get('Unit')}, 安全存量：{doc.get('Secure_Credit')} {doc.get('Unit')})")
        print("\n\n")

# Uncomment the following lines to run the automation scripts

# Launch Chrome CDP
Automation.chrome_CDP()

# Aliyun
# Aliyun.aliyun_CN()
# Aliyun.aliyun_INT()
# Aliyun.watermelon_aliyun_INT()
# Aliyun.aliyun_INT_RAM()
# Aliyun.watermelon_aliyun_INT_RAM()

# Tencent
# Tencent.tencent_CN()
# Tencent.tencent_CN_SUB()
# Tencent.tencent_INT()
# Tencent.tencent_INT_CAM()
# Tencent.tencent_ven295()

# Huawei
# Huawei.huawei_OPSADMIN()
# Huawei.huawei()

# Ucloud
# Ucloud.ucloud()

# Other
# Other_Cloud.gname()
# Other_Cloud.s211()
# Other_Cloud.byteplus()
# Other_Cloud.sms_man()

# Zentao & Noctool
# Zentao_Noctool.zentaowater()
# Zentao_Noctool.noctoolwater()
# Zentao_Noctool.low_water()