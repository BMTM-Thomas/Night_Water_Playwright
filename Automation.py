import re
import os
import time
import atexit
import random
import certifi
import requests
import pyautogui
import pyperclip
import subprocess
from PIL import ImageGrab
from List_Zentao import *
from bson import ObjectId 
from List_Noctool import *
from datetime import datetime
from dotenv import load_dotenv
from datetime import timedelta
from pymongo import MongoClient
from api.gmail_api.reader import *
from api.openai_api.auth import *
from bson.objectid import ObjectId  
from AppKit import NSPasteboard, NSPasteboardTypePNG
from playwright.sync_api import sync_playwright, expect

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
        """, timeout=0)

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

# Plawright Automation Settings
class Automation:

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
    
    # Chrome CDP 
    chrome_proc = None
    @classmethod
    def chrome_CDP(cls):

        # User Profile
        USER_DATA_DIR = "/Users/n02-19/PlaywrightProfile"  # User Profile

        # Step 1: Start Chrome normally
        cls.chrome_proc = subprocess.Popen([
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "--remote-debugging-port=9222",
            "--disable-session-crashed-bubble",
            "--hide-crash-restore-bubble",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={USER_DATA_DIR}",  # User Profile
        ],
        stdout=subprocess.DEVNULL,  # ✅ hide chrome cdp logs
        stderr=subprocess.DEVNULL   # ✅ hide chrome cdp logs
        )
        print("Chrome launched.....")
    
        # wait for Chrome CDP launch...
        cls.wait_for_cdp_ready()

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

    # Peform Drag and Drop (ALI_INT)
    @staticmethod
    def human_drag_slider(page):

        # --- Step 1: Try to find iframe ---
        iframe_locator = "iframe#alibaba-login-box"
        if page.locator(iframe_locator).count() > 0:
            # Slider inside iframe
            root = page.frame_locator(iframe_locator)
            # Check for nested iframe
            if root.locator("iframe#baxia-dialog-content").count() > 0:
                root = root.frame_locator("iframe#baxia-dialog-content")
        else:
            # No iframe
            root = page

        # --- Step 2: Locate slider handle ---
        slider = root.locator("#nc_1_n1z")
        slider.wait_for(state="visible")

        # --- Step 3: Get bounding box and track width ---
        box = slider.bounding_box()
        start_x = box["x"] + box["width"] / 2
        start_y = box["y"] + box["height"] / 2

        # --- Step 4: Perform human-like drag ---
        distance =  260
        page.mouse.move(start_x, start_y)
        page.mouse.down()
        steps = 25

        for i in range(steps):
            t = (i + 1) / steps
            x = start_x + distance * t + random.uniform(-2, 2)
            y = start_y + random.uniform(-1, 1)
            page.mouse.move(x, y, steps=1)
            time.sleep(random.uniform(0.01, 0.02))

        page.mouse.up()

    # Perform Drag and Drop (ALI_RAM)
    def human_drag_slider_2(page):

        # Step 1: Get the iframe
        iframe_locator = page.frame_locator("iframe#baxia-dialog-content")

        # Step 2: Locate the slider handle inside iframe
        slider = iframe_locator.locator("#nc_1_n1z")
        slider.wait_for(state="visible")

        # Step 3: Get bounding box for the slider handle
        box = slider.bounding_box()
        start_x = box["x"] + box["width"] / 2
        start_y = box["y"] + box["height"] / 2

        # Step 4: Perform drag
        distance = 800
        page.mouse.move(start_x, start_y)
        page.mouse.down()
        steps = 80

        for i in range(steps):
            t = (i + 1) / steps
            x = start_x + distance * t + random.uniform(-2, 2)
            y = start_y + random.uniform(-1, 1)
            page.mouse.move(x, y, steps=1)
            time.sleep(random.uniform(0.01, 0.02))

        page.mouse.up()

    # Aliyun 中国站
    @classmethod
    def aliyun_CN(cls):
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
            page = context.pages[0] if context.pages else context.new_page()
            page.goto("https://account.aliyun.com/login/login.htm?oauth_callback=https://usercenter2.aliyun.com/home", wait_until="domcontentloaded")

            # if is "RAM 用户登录" then click "主账号登录", else skip
            try:
                page.wait_for_selector("//h3[contains(text(),'RAM 用户登录')]", timeout=4000)
                __class__.red_Check(page.locator("//h3[contains(text(),'RAM 用户登录')]"), "在 'RAM 用户登录' 切换到 '主账号登录'")  # Wait for "RAM 用户登录" to be appear
                # delay 0.5second
                page.wait_for_timeout(500)
                # Click "主账号登录"
                __class__.red_Check(page.locator("//span[contains(text(),'主账号登录')]"), "Click '立即登录'")
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
                    # Wait for "可用额度" 
                    __class__.red_Check(page.locator("//span[@class='sc-jWgTtR leLjBy'][contains(text(),'可用额度')]"), "Wait '可用额度'")
                    
                    # Extract Credit
                    __class__.red_Check(page.locator("//span[@class='amount']//span[1]"), "Extract Credit '费用'")
                    credit = page.locator("//span[@class='amount']//span[1]").text_content() 
                else:
                    # Wait for "账户可用额度"
                    __class__.red_Check(page.locator("//div[@class='label'][contains(text(),'账户可用额度')]"), "Wait '账户可用额度'")
                    
                    # Wait for *
                    expect(page.locator("//div[@id='home-overview-availableAmount']//div[@class='money']")).not_to_have_text("*", timeout=0)

                    # Extract Credit
                    __class__.red_Check(page.locator("//div[@id='home-overview-availableAmount']//div[@class='money']"), "Extract Credit '账户可用额度'")
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
                
                # hover to menu
                __class__.red_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!'")
                page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # if hover menu doesnt appear, rehover again
                while True:
                    try:
                        # Wait for "权限与安全" to be appear
                        page.locator("//span[contains(text(),'权限与安全')]").wait_for(timeout=1000) 
                        __class__.red_Check(page.locator("//span[contains(text(),'权限与安全')]"), "Wait '权限与安全'")
                        break
                    except:
                        # Mouse Click
                        pyautogui.click(x=1267, y=217)
                        # delay 0.5second
                        page.wait_for_timeout(500)
                        # hover to menu
                        __class__.red_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu'")
                        page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # delay 0.5second
                page.wait_for_timeout(500)

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # Click "退出登录" Logout
                __class__.red_Check(page.locator("//a[contains(text(),'退出登录')]"), "退出登录")
                page.locator("//a[contains(text(),'退出登录')]").click(force=True)

                # delay 3seconds
                page.wait_for_timeout(3000)

                page.goto("https://account.aliyun.com/login/login.htm?oauth_callback=https://usercenter2.aliyun.com/home", wait_until="domcontentloaded", timeout= 0)

                # delay 3seconds
                page.wait_for_timeout(3000)
    
    # Aliyun 国际站
    @classmethod
    def aliyun_INT(cls):
        try:
            with sync_playwright() as p: 
                
                # MongoDB ID
                m_id = 0

                # Launch MongoDB Atlas
                collection = __class__.mongodb_atlas()

                # Connect to running Chrome
                browser = p.chromium.connect_over_cdp("http://localhost:9222")
                context = browser.contexts[0] if browser.contexts else browser.new_context()

                # Open a new browser page
                page = context.pages[0] if context.pages else context.new_page()
                page.goto("https://account.alibabacloud.com/login/login.htm?oauth_callback=https%3A%2F%2Fusercenter2-intl.console.alibabacloud.com%2Fbilling%2F#/account/overview", wait_until="domcontentloaded")
                
                # if is "RAM 用户登录" then click "主账号登录", else skip
                try:
                    page.wait_for_selector("//h3[contains(text(),'RAM 用户登录')]", timeout=4000)
                    __class__.red_Check(page.locator("//h3[contains(text(),'RAM 用户登录')]"), "Wait 'RAM 用户登录'")
                    # delay 0.5second
                    page.wait_for_timeout(500)
                    # Click "主账号登录"
                    __class__.red_Check(page.locator("//span[contains(text(),'主账号登录')]"), "Wait '主账号登录'")
                    page.locator("//span[contains(text(),'主账号登录')]").click()
                    # delay 0.5second
                    page.wait_for_timeout(500)
                    # page go to a link
                    page.goto("https://account.alibabacloud.com/login/login.htm?oauth_callback=https%3A%2F%2Fusercenter2-intl.console.alibabacloud.com%2Fbilling%2F#/account/overview")
                except:
                    pass

                for ven_id in aliyun_INT_ID:
                    
                    # Freeze scroll to avoid auto-scrolling
                    try:
                        page.add_style_tag(content="html,body{overflow:hidden !important}")
                    except Exception:
                        pass 

                    ## Get iframe
                    iframe = page.frame_locator("//iframe[@id='alibaba-login-box']")

                    ## Wait for "登录" to be appear
                    __class__.red_Check(iframe.locator("//input[@id='fm-login-submit']"), "Wait '登录'")

                    # Wait for “请输入密码” right hand side lastpass logo appear
                    image_vault = None
                    while image_vault is None:
                        image_vault = pyautogui.locateOnScreen("./image/ali_int_wait_lastpass.png", grayscale = True)
                    
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
                    __class__.red_Check(iframe.locator("#fm-login-submit"), "Click '登录'")
                    iframe.locator('#fm-login-submit').click()

                    # delay 4.0seconds
                    page.wait_for_timeout(4000)

                    # Drag and Drop Appear (Login appear)
                    while True:
                        #  if image found do something, else will error and stop
                        if pyautogui.locateOnScreen('./image/alidnd.png') is not None:
                            
                            # drag and drop
                            cls.human_drag_slider(page)  

                            # delay 1.5seconds
                            page.wait_for_timeout(1500)
        
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
                            ## Click "登录" to Login
                            try:
                                iframe.locator('#fm-login-submit').click(timeout=500)
                            except:
                                pass 
                            break
                    
                    # If Drag and Drop Appear (Sorry, we have detected unusual traffic from your network.)
                    while True:
                        try: 
                            expect(page.locator("text=Sorry, we have detected unusual traffic from your network.")) .to_be_visible(timeout=500)
                            page.reload()
                        except:
                            break

                    # Wait "正常" to be appear
                    __class__.red_Check(page.locator("//span[contains(text(),'正常')]"), "Wait '正常'")
                    
                    # Extract Credit
                    __class__.red_Check(page.locator("//div[@class='ng-binding']"), "Extract Credit ‘费用’")
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
                    
                    # delay 0.3second
                    page.wait_for_timeout(300)

                    # hover to menu
                    __class__.red_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!")
                    page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                    # if hover menu doesnt appear, rehover again
                    while True:
                        try:
                            # Wait for "安全设置" to be appear
                            expect(page.locator("//span[contains(text(),'安全设置')]")).to_be_visible(timeout = 1000) 
                            __class__.red_Check(page.locator("//span[contains(text(),'安全设置')]"), "Wait '安全设置'")
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
                    page.locator("//a[contains(text(),'退出登录')]").click(force=True)
                    
                    # delay 3second
                    page.wait_for_timeout(3000)

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(11111)

    # Watermelon Aliyun 国际站
    @classmethod
    def watermelon_aliyun_INT(cls):
        with sync_playwright() as p: 
                    
            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
            page.goto("https://account.alibabacloud.com/login/login.htm?oauth_callback=https%3A%2F%2Fusercenter2-intl.console.alibabacloud.com%2Fbilling%2F#/account/overview", wait_until="domcontentloaded")

            # if is "RAM 用户登录" then click "主账号登录", else skip
            try:
                page.wait_for_selector(":has-text('RAM 用户登录')", timeout=4000)
                __class__.red_Check(page.locator(":has-text('RAM 用户登录')"), "Wait 'RAM 用户登录'")
                # delay 0.5second
                page.wait_for_timeout(500)
                # Click "主账号登录"
                __class__.red_Check(page.locator("//span[contains(text(),'主账号登录')]"), "Wait '主账号登录'")
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

                ## Wait for "登录" to be appear
                __class__.red_Check(iframe.locator("//input[@id='fm-login-submit']"), "Wait '简体中文'")
                
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
                __class__.red_Check(iframe.locator("#fm-login-submit"), "Click '登录'")
                iframe.locator('#fm-login-submit').click()

                # delay 4seconds
                page.wait_for_timeout(4000)

                # If Drag and Drop Appear
                while True:
                    #  if image found do something, else will error and stop
                    if pyautogui.locateOnScreen('./image/alidnd.png') is not None:
                        
                        # drag and drop
                        cls.human_drag_slider(page)  

                        # delay 1.5seconds
                        page.wait_for_timeout(1500)
    
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
                
                # If Drag and Drop Appear (Sorry, we have detected unusual traffic from your network.)
                while True:
                        try: 
                            expect(page.locator("text=Sorry, we have detected unusual traffic from your network.")) .to_be_visible(timeout=500)
                            page.reload()
                        except:
                            break
                
                ## Click "登录" to Login
                try:
                    iframe.locator('#fm-login-submit').click(timeout=500)
                except:
                    pass    
                
                # Wait "VISA Logo" to be appear
                __class__.red_Check(page.locator("//span[@class='payment-cardrand-visa']"), "Wait 'VISA Logo Appear'")

                # Check if overdue payment
                try:
                    page.wait_for_selector("//span[@ng-bind-html='item']", timeout=1500)
                    __class__.red_Check(page.locator("//span[@ng-bind-html='item']"), "欠费 欠费 欠费 欠费 欠费 欠费")
                    overdue = page.locator("//span[@ng-bind-html='item']").text_content()
                    print(f"{ven_id}= ", overdue)   
                except:
                    pass

                # Screenshot
                ImageGrab.grab().save(f'./watermelon/{ven_id}.png')

                # Wait for "主账号" to be appear
                page.locator("(//div[@class='sc-taltu8-3 CB-cquEbr'])[1]").wait_for(timeout=0) 
                __class__.red_Check(page.locator("(//div[@class='sc-taltu8-3 CB-cquEbr'])[1]"), "Wait '主账号'")

                # hover to menu
                __class__.red_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!")
                page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # if hover menu doesnt appear, rehover again
                while True:
                    try:
                        # Wait for "安全设置" to be appear
                        expect(page.locator("//span[contains(text(),'安全设置')]")).to_be_visible(timeout = 1000) 
                        __class__.red_Check(page.locator("//span[contains(text(),'安全设置')]"), "Wait '安全设置'")
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

                # Click "退出登录" Logout
                __class__.red_Check(page.locator("//a[contains(text(),'退出登录')]"), "退出登录")
                page.locator("//a[contains(text(),'退出登录')]").click(force=True)

                # delay 3seconds
                page.wait_for_timeout(3000)

    # Aliyun 国际版【RAM】    
    @classmethod
    def aliyun_INT_RAM(cls):
        with sync_playwright() as p: 
            
            # MongoDB ID
            m_id = 0    

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()

            # Navigate to Aliyun Ram
            page.goto("https://signin.alibabacloud.com/5256975880117898.onaliyun.com/login.htm?callback=https%3A%2F%2Fusercenter2-intl.aliyun.com%2Fbilling%2F%23%2Faccount%2Foverview#/main", wait_until="domcontentloaded")
            
            # delay 1second
            page.wait_for_timeout(1000)

           # For loop
            for ven_id in aliyun_INT_RAM_ID:
                
                # Wait for lastpass vault button image to appear
                image_vault = None
                while image_vault is None:
                    page.wait_for_timeout(1500)
                    image_vault = pyautogui.locateOnScreen("./image/vault_00.png", grayscale = True)
                    # If image_vault is None, reload page
                    if image_vault is None:
                        page.reload()
                        page.wait_for_timeout(1000)
                    else:
                        break

                # wait for "RAM 用户登录" to be appear
                __class__.red_Check(page.locator("//h3[contains(text(),'RAM 用户登录')]"), "Wait 'RAM 用户登录'")

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

                # Click "下一步" 
                __class__.red_Check(page.locator("//button[@type='button']"), "Wait '下一步'")
                page.locator('//button[@type="button"]').click()

                # Wait for "*用户密码" appear
                __class__.red_Check(page.locator("//label[contains(text(),'用户密码')]"), "Wait '*用户密码'")

                # delay 1.5second
                page.wait_for_timeout(1500)

                # Click “登录”
                __class__.red_Check(page.locator("//button[@type='submit']"), "Click '登录'")
                page.locator('//button[@type="submit"]').click(timeout=1000)

                # Wait for "验证安全邮箱" appear
                __class__.red_Check(page.locator("//h3[contains(text(),'验证安全邮箱')]"), "Wait '验证安全邮箱'")

                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "获取验证码" 
                page.locator('//span[contains(text(),"获取验证码")]').click()

                # Call Gmail APi and get Verification code
                service = create_service("credentials.json", "gmail", "v1", ['https://www.googleapis.com/auth/gmail.readonly'])
                if code := wait_for_alibaba_verification_code(service):
                    print("✅ Verification Code:", code)

                # Click "x mark"
                page.locator('//i[@class="next-icon next-icon-close next-xs"]').click()
                
                # Fill Verification Code
                page.fill("//input[@id='EMAIL_CODE']", code)

                # delay 0.5second
                page.wait_for_timeout(500) 

                # Click "提交验证码"
                __class__.red_Check(page.locator("//button[@type='submit']"), "Click '提交验证码'")
                page.locator('//button[@type="submit"]').click()

                # Wait for "正常" appear
                __class__.red_Check(page.locator("//span[contains(text(),'正常')]"), "Wait '正常'")

                # Mouse Click
                pyautogui.click(x=1100, y=287)
                
                # Extract Credit
                __class__.red_Check(page.locator("//div[@class='ng-binding']"), "Extract Credit '费用'")
                credit = page.locator(f"//div[@class='ng-binding']").text_content()

                # Replace
                credit = credit.replace(' USD', '')

                # MongoDB Update Data
                mangos_id = {'_id': ObjectId(aliyun_INT_RAM_MONGODB[m_id])}
                collection.update_one(mangos_id, {"$set": {"Credit": credit}})
                print(f"{ven_id}= {credit}\n")
                # mongdb+id +1
                m_id += 1

                # Wait for "RAM 用户" to be appear
                __class__.red_Check(page.locator("(//div[@class='sc-taltu8-3 CB-cquEbr'])[1]"), "Wait 'RAM 用户'")

                # delay 0.3second
                page.wait_for_timeout(300)

                # hover to menu
                __class__.red_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!")
                page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # if hover menu doesnt appear, rehover again
                while True:
                    try:
                        # Wait for "安全管控" to be appear
                        expect(page.locator("//span[contains(text(),'安全管控')]")).to_be_visible(timeout = 1000) 
                        __class__.red_Check(page.locator("//span[contains(text(),'安全管控')]"), "Wait '安全管控'")
                        break
                    except:
                        # Mouse Click
                        pyautogui.click(x=1267, y=217)
                        # delay 0.3second
                        page.wait_for_timeout(300)
                        # hover to menu
                        page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # delay 0.3second
                page.wait_for_timeout(500)

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # Click "退出登录" Logout
                __class__.red_Check(page.locator("//a[contains(text(),'退出登录')]"), "Click '退出登录'")
                page.locator("//a[contains(text(),'退出登录')]").click(force=True)

                # delay 3second
                page.wait_for_timeout(3000)

    # Watermelon Aliyun 国际站【RAM】    
    @classmethod
    def watermelon_aliyun_INT_RAM(cls):
        with sync_playwright() as p: 

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()

            # Navigate to Aliyun Ram
            page.goto("https://signin.alibabacloud.com/5256975880117898.onaliyun.com/login.htm?callback=https%3A%2F%2Fusercenter2-intl.aliyun.com%2Fbilling%2F%23%2Faccount%2Foverview#/main", wait_until="domcontentloaded")
            
            # delay 1second
            page.wait_for_timeout(1000)

            # For loop
            for ven_id in watermelon_aliyun_INT_RAM_ID:
                
                # Wait for lastpass vault button image to appear
                image_vault = None
                while image_vault is None:
                    page.wait_for_timeout(1500)
                    image_vault = pyautogui.locateOnScreen("./image/vault_00.png", grayscale = True)
                    # If image_vault is None, reload page
                    if image_vault is None:
                        page.reload()
                        page.wait_for_timeout(1000)

                # wait for "RAM 用户登录" to be appear
                __class__.red_Check(page.locator("//h3[contains(text(),'RAM 用户登录')]"), "Wait 'RAM 用户登录'")

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

                # Click "下一步" 
                __class__.red_Check(page.locator("//button[@type='button']"), "Wait '下一步'")
                page.locator('//button[@type="button"]').click()

                # Wait for "*用户密码" appear
                __class__.red_Check(page.locator("//label[contains(text(),'用户密码')]"), "Wait '*用户密码'")

                # delay 1.5second
                page.wait_for_timeout(1500)

                # Click “登录”
                __class__.red_Check(page.locator("//button[@type='submit']"), "Click '登录'")
                page.locator('//button[@type="submit"]').click(timeout=1000)

                # delay 3seconds
                page.wait_for_timeout(3000)

                # Drag and Drop Appear (after 下一步 appear)
                while True:
                    #  if image found do something, else will error and stop
                    if pyautogui.locateOnScreen('./image/alidnd7_2.png') is not None:
    
                        cls.human_drag_slider_2(page)  

                        # delay 3seconds
                        page.wait_for_timeout(3000)

                    else:
                        break

                # Wait for "验证安全邮箱" appear
                __class__.red_Check(page.locator("//h3[contains(text(),'验证安全邮箱')]"), "Wait '验证安全邮箱'")

                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "获取验证码" 
                page.locator('//span[contains(text(),"获取验证码")]').click()

                # delay 0.5second
                page.wait_for_timeout(500) 

                # Call Gmail APi and get Verification code
                service = create_service("credentials.json", "gmail", "v1", ['https://www.googleapis.com/auth/gmail.readonly'])
                if code := wait_for_alibaba_verification_code(service):
                    print("✅ Verification Code:", code)

                # Click "x mark"
                page.locator('//i[@class="next-icon next-icon-close next-xs"]').click()
                
                # Fill Verification Code
                page.fill("//input[@id='EMAIL_CODE']", code)

                # delay 0.5second
                page.wait_for_timeout(500) 

                # Click "提交验证码"
                page.locator('//button[@type="submit"]').click()

                # Wait for "本月消费概览" appear
                __class__.red_Check(page.locator("//span[contains(text(),'本月消费概览')]"), "Wait ‘本月消费概览'")

                # Mouse Click
                pyautogui.click(x=1100, y=287)

                # Wait for "VISA" to be appear
                __class__.red_Check(page.locator("//span[@class='payment-cardrand-visa']"), "Wait ‘VISA Logo Appear'")

                # Check if overdue payment
                try:
                    overdue = page.locator("//p[@ng-repeat='item in vm.topTipsArr']").wait_for(timeout=2000)
                    __class__.red_Check(page.locator("//p[@ng-repeat='item in vm.topTipsArr']"), "欠费 欠费 欠费 欠费 欠费 欠费'")
                    print(f"{ven_id}= ", overdue)   
                except:
                    pass

                # Screenshot
                ImageGrab.grab().save(f'./watermelon/{ven_id}.png')
                
                # Wait for "RAM 用户" to be appear
                __class__.red_Check(page.locator("//div[@class='sc-taltu8-3 CB-cquEbr']"), "Wait 'RAM 用户'")

                # delay 0.3second
                page.wait_for_timeout(300)

                # hover to menu
                __class__.red_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), "Hover to Menu!")
                page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # if hover menu doesnt appear, rehover again
                while True:
                    try:
                        # Wait for "安全管控" to be appear
                        expect(page.locator("//span[contains(text(),'安全管控')]")).to_be_visible(timeout = 1000) 
                        __class__.red_Check(page.locator("//span[contains(text(),'安全管控')]"), "Wait '安全管控'")
                        break
                    except:
                        # Mouse Click
                        pyautogui.click(x=1100, y=287)
                        # delay 0.5second
                        page.wait_for_timeout(500)
                        # hover to menu
                        __class__.red_Check(page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']"), 'Hover Menu')
                        page.locator("//div[@class='sc-168k6tv-0 sc-taltu8-0 CB-dQgHzF CB-hvlcZA']").hover()

                # Wait for "安全管控" to be appear
                __class__.red_Check(page.locator("//span[contains(text(),'安全管控')]"), "Wait '安全管控'")

                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "退出登录" Logout
                __class__.red_Check(page.locator("//a[contains(text(),'退出登录')]"), "Click '退出登录'")
                page.locator("//a[contains(text(),'退出登录')]").click(force=True)

                # delay 0.5second
                page.wait_for_timeout(500)

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

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Close all existing tabs (to avoid Gmail or wrong pages)
            for pg in context.pages:
                pg.close()

            # Create a new browser tab
            page = context.pages[0] if context.pages else context.new_page()
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
            page.locator("//div[@class='accsys-tp-tabs__item-label'][contains(text(),'邮箱登录')]").click()

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

                        prompt = "请根据截图中的提示，指出要点击的格子，例如 '1-2, 2-3'"
                        response_text = ask_gpt_about_image('./晚班水位/ven182.png', prompt)
                        print("🧠 GPT Response:", response_text)

                        extract_positions_and_click(response_text)
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
            page.hover("div.sdk-nav-v2-nav-user-info-account")

            # delay 0.5second
            page.wait_for_timeout(500)

            # if hover menu doesnt appear, rehover again
            while True:
                try:
                    # Wait for "安全设置" to be appear
                    page.locator("//span[contains(text(),'安全设置')]").is_visible()
                    break
                except:
                    # Mouse Click
                    pyautogui.click(x=1267, y=217)
                    # delay 0.3second
                    page.wait_for_timeout(300)
                    # hover to menu
                    page.hover("div.sdk-nav-v2-nav-user-info-account")
                    # delay 1second
                    page.wait_for_timeout(500)

            # Screenshot
            ImageGrab.grab().save('./晚班水位/ven182.png')

            # delay 0.5second
            page.wait_for_timeout(500)

            # Click "logout" to Login
            page.locator("//button[contains(text(),'退出')]").click()

            # delay 1.5second
            page.wait_for_timeout(1500)

    # 腾讯云【中国站】 子用户登录
    @classmethod
    def tencent_CN_SUB(cls):
        with sync_playwright() as p:  
            
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
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
            page.hover("div.sdk-nav-v2-nav-user-info-account")

            # delay 0.5second
            page.wait_for_timeout(500)

            # if hover menu doesnt appear, rehover again
            while True:
                try:
                    # Wait for "安全设置" to be appear
                    page.locator("//span[contains(text(),'安全设置')]").is_visible()
                    break
                except:
                    # Mouse Click
                    pyautogui.click(x=1267, y=217)
                    # delay 0.3second
                    page.wait_for_timeout(300)
                    # hover to menu
                    page.hover("div.sdk-nav-v2-nav-user-info-account")
                    # delay 1second
                    page.wait_for_timeout(500)

            # delay 0.5second
            page.wait_for_timeout(500)

            # Screenshot
            ImageGrab.grab().save('./晚班水位/ven322.png')

            # delay 0.5second
            page.wait_for_timeout(500)

            # Click "logout" to Login
            page.locator("//button[contains(text(),'退出')]").click()

            # delay 1.5second
            page.wait_for_timeout(1500)

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
            page = context.pages[0] if context.pages else context.new_page()

            # Navigate to Tencent Cloud         
            page.goto("https://www.tencentcloud.com/zh/account/login?s_url=https://console.tencentcloud.com/expense/rmc/accountinfo", wait_until="domcontentloaded")
            
            # delay 1second
            page.wait_for_timeout(1000)
            
            # if is "CAM用户登录" then click "切换登录方式", else skip
            try:
                if page.locator("div.LoginCommonBox_clg-mod-title__gpSTl.tcas-login-panel__box-title:has-text('CAM用户登录')").is_visible():
                    # Click "主账号登录"
                    page.locator("//button[contains(text(),'主账号登录')]").click()
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

                # delay 0.5second
                page.wait_for_timeout(500)

                # if Login Failed, refresh website and try login again
                if page.locator("//p[contains(text(),'登录失败，请重试')]").is_visible():
                    page.reload()
                    # wait for "邮箱登录" to be appear
                    page.locator("//div[@class='LoginCommonBox_clg-mod-title__gpSTl tcas-login-panel__box-title']").wait_for(timeout=0) 
                    # delay 1second
                    page.wait_for_timeout(1000)
                    # Click "登录" to Login
                    page.locator("//button[@type='submit']//span[contains(text(),'登录')]").click()
                else:
                    pass
    
                # delay 3seconds
                page.wait_for_timeout(3000)

                # Verify if "登录验证" is present
                while True:
                    # if "请输入通过邮件发送的验证码" appear
                    if page.locator("//div[@class='VerifyBox_mfa-international-verify-card__phone-label__K98Fv tcas-mfa-account-tip']").is_visible():
                        
                        # wait for "请输入通过邮件发送的验证码" to be appear
                        page.locator("//div[@class='VerifyBox_mfa-international-verify-card__phone-label__K98Fv tcas-mfa-account-tip']").wait_for(timeout=0) 

                        # delay 1.5 second
                        page.wait_for_timeout(1500)

                        # Click "发送验证码", but sometime it auto click already    
                        try:                             
                            page.locator("//a[contains(text(),'发送验证码')]").wait_for(timeout=1000)
                            page.wait_for_timeout(1000)
                            page.locator("//a[contains(text(),'发送验证码')]").click()
                            page.wait_for_timeout(2000)
                        except:
                            pass
                        
                        # Check whether have 3 dots loading image appear
                        if pyautogui.locateOnScreen("./image/tencent_3_dots.png", grayscale=True):
                            page.wait_for_timeout(5000)
                        else:
                            pass
                        
                        # wait for CAPTCHA "image验证" to be appear
                        while True:
                            # set iframe
                            iframe = page.frame_locator("//iframe[@id='tcaptcha_iframe_dy']")

                            # Check whether Captcha is present
                            try:
                                # Wait up to 1 second for element to appear
                                iframe.locator("//span[@id='pHeaderTitle']").wait_for(timeout=1000)
                                title = iframe.locator("//span[@id='pHeaderTitle']").text_content()
                            except:
                                title = None

                            # if title contains "选择" or "图片", then it is a captcha challenge
                            if title and "选择" in title and "图片" in title:
                                print(f"🛑 Captcha challenge detected: {title}")

                                # Chatgpt solve captcha...
                                page.wait_for_timeout(2000)
                                screenshot = pyautogui.screenshot(region=(619, 296, 360, 359))
                                screenshot.save('./晚班水位/ven182.png')

                                prompt = "请根据截图中的提示，指出要点击的格子，例如 '1-2, 2-3'"
                                response_text = ask_gpt_about_image('./晚班水位/ven182.png', prompt)
                                print("🧠 GPT Response:", response_text)

                                extract_positions_and_click(response_text)
                                iframe.locator("//button[@id='verifyBtn']").click()

                                # Mouse mouse to prevent it block the screenshot, causing chatgpt unable to solve captcha
                                pyautogui.click(x=395, y=309)

                                # delay 3 seconds
                                page.wait_for_timeout(3000)

                                # Check again x times
                                continue
                            else:
                                break
                        
                        pyautogui.click(348,571)

                        # Call Gmail APi and get Verification code
                        service = create_service("credentials.json", "gmail", "v1", ['https://www.googleapis.com/auth/gmail.readonly'])
                        if code := wait_for_tencent_verification_code(service):
                            print("Verification Code:", code)

                        # Copy Paste code
                        pyperclip.copy(code)
                        pyautogui.keyDown('command')
                        pyautogui.press('v')
                        pyautogui.keyUp('command')

                        break
                    else:
                        if page.locator("//h2[contains(text(),'账户信息')]").is_visible():
                            break 
                        else: 
                            continue

                # wait for "账户信息" to be appear
                page.locator("//h2[contains(text(),'账户信息')]").wait_for(timeout=0) 
                # wait for "可用额度" to be appear
                page.locator("//h3[contains(text(),'可用额度')]").wait_for(timeout=0) 
                # wait for "0 张 （7日内到期0张）" to be appear
                page.locator("(//div[@class='data-mod inline'])[2]").wait_for(state="visible", timeout=5000)

                # delay 2.5second
                page.wait_for_timeout(2500)

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
                page.hover("a.fn-sdk-nav-dropdown-item.sdk-nav-account")

                # delay 0.5second   
                page.wait_for_timeout(500)

                # if hover menu doesnt appear, rehover again
                while True:
                    try:
                        # Wait for "安全设置" to be appear
                        page.locator("//a[contains(text(),'安全设置')]").is_visible()
                        break
                    except:
                        # Mouse Click
                        pyautogui.click(x=1267, y=217)
                        # delay 0.3second
                        page.wait_for_timeout(300)
                        # hover to menu
                        page.hover("a.fn-sdk-nav-dropdown-item.sdk-nav-account")
                        # delay 1second
                        page.wait_for_timeout(500)

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "logout" to Logout
                page.locator("//a[contains(text(),'退出')]").click()

                # delay 2second
                page.wait_for_timeout(2000)

    # 腾讯云【国际站】CAM用户登录
    @classmethod
    def tencent_INT_CAM(cls):
        with sync_playwright() as p:  
            
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Close all existing tabs (to avoid Gmail or wrong pages)
            for pg in context.pages:
                pg.close()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
            
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
                page.hover("a.fn-sdk-nav-dropdown-item.sdk-nav-account")

                # delay 0.5second
                page.wait_for_timeout(500)

                # if hover menu doesnt appear, rehover again
                while True:
                    try:
                        # Wait for "安全设置" to be appear
                        page.locator("//a[contains(text(),'安全设置')]").is_visible()
                        break
                    except:
                        # Mouse Click
                        pyautogui.click(x=1267, y=217)
                        # delay 0.3second
                        page.wait_for_timeout(300)
                        # hover to menu
                        page.hover("a.fn-sdk-nav-dropdown-item.sdk-nav-account")
                        # delay 0.5second
                        page.wait_for_timeout(500)

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # delay 1second
                page.wait_for_timeout(1000)

                # Click "logout" to Login
                page.locator("//a[contains(text(),'退出')]").click()

                # delay 1.5second
                page.wait_for_timeout(1500)
    
    # 腾讯云【国际站】ven295 (Tencent Website Bug)
    @classmethod
    def tencent_ven295(cls):
        with sync_playwright() as p:  
                    
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
            page.goto("https://intl.cloud.tencent.com/zh/account/login?s_url=https%3A%2F%2Fconsole.intl.cloud.tencent.com%2Fexpense%2Frmc%2Faccountinfo", wait_until="domcontentloaded")

            # if is "CAM用户登录" then click "主账号登录", else skip
            try:
                text = page.locator("//div[@class='LoginCommonBox_clg-mod-title__gpSTl tcas-login-panel__box-title']").text_content()
                if "CAM用户登录" in text:
                    page.locator("//button[contains(text(),'主账号登录')]").click()
            except:
                pass

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
            print(f"ven295= {credit}")
            # mongdb+id +1
            m_id += 1

            # hover to menu
            page.hover("a.fn-sdk-nav-dropdown-item.sdk-nav-account")

            # delay 0.5second
            page.wait_for_timeout(500)

            # if hover menu doesnt appear, rehover again
            while True:
                try:
                    # Wait for "安全设置" to be appear
                    page.locator("//a[contains(text(),'安全设置')]").is_visible()
                    break
                except:
                    # Mouse Click
                    pyautogui.click(x=1267, y=217)
                    # delay 0.3second
                    page.wait_for_timeout(300)
                    # hover to menu
                    page.hover("a.fn-sdk-nav-dropdown-item.sdk-nav-account")
                    # delay 1second
                    page.wait_for_timeout(500)

            # Screenshot
            ImageGrab.grab().save('./晚班水位/ven295.png')

            # delay 0.5second
            page.wait_for_timeout(500)

            # Click "logout" to Login
            page.locator("//a[contains(text(),'退出')]").click()

            # delay 1.5second
            page.wait_for_timeout(1500)

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

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
            
            for ven_id in huawei_OPSADMIN_ID:

                # Huawei OPSADMIN Login
                page.goto(Huawei_Webpage[m_id], wait_until="domcontentloaded")

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
                page.hover("ul.modules-user-info-user-info-menu-wrapper-user-info-multi-user-info")

                # delay 0.5second
                page.wait_for_timeout(500)

                # if hover menu doesnt appear, rehover again
                while True:
                    try:
                        # Wait for "安全设置" to be appear
                        page.locator("//a[@id='cf_user_info_securitySettings_common']").is_visible()
                        break
                    except:
                        # Mouse Click
                        pyautogui.click(x=1267, y=217)
                        # delay 0.3second
                        page.wait_for_timeout(300)
                        # hover to menu
                        page.hover("ul.modules-user-info-user-info-menu-wrapper-user-info-multi-user-info")
                        # delay 1second
                        page.wait_for_timeout(500)

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "logout" to Login
                page.locator("//span[@id='cf_user_info_logout']").click()

                # delay 3second
                page.wait_for_timeout(3000)

    # Huawei
    @classmethod
    def huawei(cls):
        with sync_playwright() as p:  
            
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
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

                # hover to menu
                page.hover("ul.modules-user-info-user-info-menu-wrapper-user-info-multi-user-info")

                # delay 0.5second
                page.wait_for_timeout(500)

                # if hover menu doesnt appear, rehover again
                while True:
                    try:
                        # Wait for "安全设置" to be appear
                        page.locator("//a[@id='cf_user_info_securitySettings_common']").is_visible()
                        break
                    except:
                        # Mouse Click
                        pyautogui.click(x=1267, y=217)
                        # delay 0.3second
                        page.wait_for_timeout(300)
                        # hover to menu
                        page.hover("ul.modules-user-info-user-info-menu-wrapper-user-info-multi-user-info")
                        # delay 0.5second
                        page.wait_for_timeout(500)

                # Screenshot
                ImageGrab.grab().save(f'./晚班水位/{ven_id}.png')

                # delay 0.5second
                page.wait_for_timeout(500)

                # Click "logout" to Login
                page.locator("//span[@id='cf_user_info_logout']").click()

                # delay 1second
                page.wait_for_timeout(1000)

            # delay 3second
            page.wait_for_timeout(3000)

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

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            
            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
            page.goto("https://passport.ucloud.cn/#login", wait_until="domcontentloaded")
            
            # wait for "账号登录" to be appear
            page.locator("//div[@class='social-title-left']").wait_for(timeout=0) 

            # delay 1second
            page.wait_for_timeout(1000)

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
            
            # Login, sometime button click the login already, website doesnt load to the credit page, have to click few times only successful to login
            while True:
                try:
                    # wait for "私有网络" to be appear
                    page.locator("//h2[contains(text(),'私有网络')]").wait_for(timeout=1000)
                    break
                except:
                    try:
                        # Click "登录" to Login
                        page.locator("(//button[contains(text(),'登录')])[1]").click(timeout=1000)
                    except:
                        pass

            # delay 0.5second
            page.wait_for_timeout(500)

            # Click Profile menu
            page.locator("//img[@class='header-user-icon']").click()

            # wait for "账户余额" to be appear
            page.locator("//div[contains(text(),'账户余额')]").wait_for(timeout=0) 

            # delay 3seconds
            page.wait_for_timeout(3000)

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

            # delay 1second
            page.wait_for_timeout(1000)

            # Click "logout" to Login
            page.locator("//span[contains(text(),'退出账号')]").click()

            # delay 3second
            page.wait_for_timeout(3000)

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

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
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

                # Mouse Click "X"
                pyautogui.click(x=1001, y=342)

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

                # delay 3second
                page.wait_for_timeout(3000)

    # SMS-MAN
    @classmethod
    def sms_man(cls):
        with sync_playwright() as p:  

            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
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
            
            # delay second
            page.wait_for_timeout(3000)

    # 7211.com
    @classmethod
    def s211(cls):
        with sync_playwright() as p:  
                    
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
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

            # delay 3second
            page.wait_for_timeout(3000)

    # byteplus
    @classmethod
    def byteplus(cls):
        with sync_playwright() as p:  
                    
            # MongoDB ID
            m_id = 0

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] if context.pages else context.new_page()
            page.goto("https://console.byteplus.com/auth/login/?redirectURI=https%3A%2F%2Fconsole.byteplus.com%2Ffinance%2Foverview", wait_until="domcontentloaded")
            
            for ven_id in byteplus_ID:
            
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
                credit = page.locator("//*[@id='root']/div/div[2]/div/div/div[2]/div/div[1]/div[4]/div/p[2]/span[1]").text_content()

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

                # Click "退出“ logout 
                page.locator("//button[@class='bp-nav-btn bp-nav-btn-secondary bp-nav-btn-size-default bp-nav-btn-shape-square index-module__btn--3XoR5']").click()

                # delay 3seconds
                page.wait_for_timeout(3000)
                
                # Navigate to finance page
                page.goto("https://console.byteplus.com/auth/login/?redirectURI=https%3A%2F%2Fconsole.byteplus.com%2Ffinance%2Foverview", wait_until="domcontentloaded")

# Zentaowater & Noctoolwater Automation
class Zentao_Noctool(Automation):

    @classmethod
    def noctool_ChangeAcc(cls):
        with sync_playwright() as p:  

            # Connect to running Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # Open a new browser page
            page = context.pages[0] 
            page.goto("http://10.77.1.196/workorders/list/default/", wait_until="domcontentloaded")

            time.sleep(1111111)

    # zentao 水位记录
    @classmethod
    def zentaowater(cls):
        with sync_playwright() as p:  

            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

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

                # delay 1second
                page.wait_for_timeout(1000)

                # click lastpass extension       
                pyautogui.click(x=1416, y=63)

                # Wait for image Appear
                image_vault = None
                while image_vault is None:
                    image_vault = pyautogui.locateOnScreen('./image/vault3.png', grayscale = True)
                print("Lastpass Image Vault Loaded") 

                # delay 1second
                page.wait_for_timeout(1000)
                # Mouse Click
                pyautogui.click(1176,212)   
                # delay 1second
                page.wait_for_timeout(1000)
                # Click "登入" 
                page.locator("//button[@id='submit']").click()
                # delay 1second
                page.wait_for_timeout(1000)
            except:
                pass

            ## Get iframe
            iframe = page.frame_locator("//div[@id='apps']//iframe[@id='appIframe-project']")

            ## Wait for "晚班週期性業務(複製用)" to be appear
            iframe.locator("//*[@id='datatable-taskList']/div[2]/div[1]/div/table/tbody/tr[3]/td[2]/a").wait_for(timeout=0) 

            # Mouse Click
            pyautogui.click(1563,502)

            ## Click "edit" 
            iframe.locator("//*[@id='datatable-taskList']/div[2]/div[3]/div/table/tbody/tr[1]/td/a[4]").click()

            ## Wait for "任务名称" to be appear
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

            # delay 1.5second
            page.wait_for_timeout(1500)
            
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

                    # delay 0.3second
                    page.wait_for_timeout(300)
                    
                    # Paste Image
                    pyautogui.keyDown('command')
                    pyautogui.press('v')
                    pyautogui.keyUp('command')

                    # Next Line
                    pyautogui.press('enter', presses = 2)
                    # delay 0.5 second
                    page.wait_for_timeout(500) 

            ## Click "保存" 
            iframe.locator("//button[@id='submit']").click()

            # delay 3seconds
            page.wait_for_timeout(3000)  

    # noctool 水位记录
    @classmethod
    def noctoolwater(cls):
        with sync_playwright() as p:  
        
            # Launch MongoDB Atlas
            collection = __class__.mongodb_atlas()

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

            # Flatten the nested tuples
            mongodb_id = sum(all_Cloud_MONGODB, ())
            ven_id = sum(all_Cloud_ID, ())

            for mongodb_id_items, ven_id_items, links_items in zip(mongodb_id, ven_id, n_webpage):

                # Go to the webpage
                page.goto(links_items, wait_until="domcontentloaded")

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
                search_mongodb_id = {'_id': ObjectId(mongodb_id_items)}
                documents = collection.find_one(search_mongodb_id)
                credit_value = documents.get('Credit', 'N/A') 

                # Fill credit
                page.fill('//input[@id="id_stocks"]', credit_value)
                page.keyboard.press("Enter")  

                # Yesterday record vs Today Record
                print(f"{ven_id_items}= Yesterday_Record: {pre_credit}, Today_Record: {credit_value} \n") 

                # delay 0.5second
                page.wait_for_timeout(500)

    # 检查 【安全水位】
    def low_water ():
        
        print("\n【低于安全水位】\n")
        collection = __class__.mongodb_atlas()
        documents = collection.find()

        for doc in documents:
            if float(doc.get("Credit", 0)) < float(doc.get("Secure_Credit", 0)):
                print(f"{doc.get('Ven_Machine')} 已低于安全流量 (当前存量：{doc.get('Credit')} {doc.get('Unit')}, 安全存量：{doc.get('Secure_Credit')} {doc.get('Unit')})")
        print("\n\n")

# Uncomment the following lines to run the automation scripts

# Timer, Start Time
start = time.perf_counter()

# Launch Chrome CDP
Automation.chrome_CDP()

# Aliyun
# Aliyun.aliyun_CN()
Aliyun.aliyun_INT()
Aliyun.watermelon_aliyun_INT()
# Aliyun.aliyun_INT_RAM()
# Aliyun.watermelon_aliyun_INT_RAM()

# Tencent
Tencent.tencent_CN()
Tencent.tencent_CN_SUB()
Tencent.tencent_INT()
Tencent.tencent_INT_CAM()
Tencent.tencent_ven295()
 
# Huawei
Huawei.huawei_OPSADMIN()
Huawei.huawei()

# # Ucloud
Ucloud.ucloud()

# # Other
Other_Cloud.gname()
Other_Cloud.s211()
Other_Cloud.byteplus() 
Other_Cloud.sms_man()

# # Zentao & Noctool
Zentao_Noctool.zentaowater()
# Zentao_Noctool.noctool_ChangeAcc()
Zentao_Noctool.noctoolwater()
Zentao_Noctool.low_water()


# Timer, End Time
end = time.perf_counter()
elapsed = end - start  # total seconds as float

# Convert to hours:minutes:seconds format
readable = str(timedelta(seconds=elapsed))
print("Elapsed time:", readable)